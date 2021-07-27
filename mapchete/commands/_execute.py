import logging
from multiprocessing import cpu_count
from rasterio.crs import CRS
from shapely.geometry.base import BaseGeometry
from typing import Callable, List, Tuple, Union

import mapchete
from mapchete.config import bounds_from_opts, raw_conf, raw_conf_process_pyramid

logger = logging.getLogger(__name__)


def execute(
    mapchete_config: Union[str, dict],
    zoom: Union[int, List[int]] = None,
    area: Union[BaseGeometry, str, dict] = None,
    area_crs: Union[CRS, str] = None,
    bounds: Tuple[float] = None,
    bounds_crs: Union[CRS, str] = None,
    point: Tuple[float, float] = None,
    point_crs: Tuple[float, float] = None,
    tile: Tuple[int, int, int] = None,
    overwrite: bool = False,
    mode: str = "continue",
    multi: int = None,
    max_chunksize: int = None,
    multiprocessing_start_method: str = None,
    dask_scheduler=None,
    msg_callback: Callable = None,
    as_iterator: bool = False,
) -> mapchete.Job:
    """
    Execute a Mapchete process.

    Parameters
    ----------
    mapchete_config : str or dict
        Mapchete configuration as file path or dictionary.
    zoom : integer or list of integers
        Single zoom, minimum and maximum zoom or a list of zoom levels.
    area : str, dict, BaseGeometry
        Geometry to override bounds or area provided in process configuration. Can be either a
        WKT string, a GeoJSON mapping, a shapely geometry or a path to a Fiona-readable file.
    area_crs : CRS or str
        CRS of area (default: process CRS).
    bounds : tuple
        Override bounds or area provided in process configuration.
    bounds_crs : CRS or str
        CRS of area (default: process CRS).
    point : iterable
        X and y coordinates of point whose corresponding process tile bounds will be used.
    point_crs : str or CRS
        CRS of point (defaults to process pyramid CRS).
    tile : tuple
        Zoom, row and column of tile to be processed (cannot be used with zoom)
    overwrite : bool
        Overwrite existing output.
    mode : str
        Set process mode. One of "readonly", "continue" or "overwrite".
    multi : int
        Number of processes used to paralellize tile execution.
    max_chunksize : int
        Maximum number of process tiles to be queued for each  worker. (default: 1)
    multiprocessing_start_method : str
        Method used by multiprocessing module to start child workers. Availability of methods
        depends on OS.
    msg_callback : Callable
        Optional callback function for process messages.
    as_iterator : bool
        Returns as generator but with a __len__() property.

    Returns
    -------
    mapchete.Job instance either with already processed items or a generator with known length.

    Examples
    --------
    >>> execute("foo")

    This will run the whole execute process.

    >>> for i in execute("foo", as_iterator=True):
    >>>     print(i)

    This will return a generator where through iteration, tiles are copied.

    >>> list(tqdm.tqdm(execute("foo", as_iterator=True)))

    Usage within a process bar.
    """
    mode = "overwrite" if overwrite else mode

    def _empty_callback(*args):
        pass

    msg_callback = msg_callback or _empty_callback
    multi = multi or cpu_count()

    if tile:
        tile = raw_conf_process_pyramid(raw_conf(mapchete_config)).tile(*tile)
        bounds = tile.bounds
        zoom = tile.zoom
    else:
        bounds = bounds_from_opts(
            point=point,
            point_crs=point_crs,
            bounds=bounds,
            bounds_crs=bounds_crs,
            raw_conf=raw_conf(mapchete_config),
        )

    # be careful opening mapchete not as context manager
    mp = mapchete.open(
        mapchete_config,
        mode=mode,
        bounds=bounds,
        zoom=zoom,
        area=area,
        area_crs=area_crs,
    )
    try:
        tiles_count = mp.count_tiles()
        if tile:
            msg_callback("processing 1 tile")
        else:
            msg_callback(f"processing {tiles_count} tile(s) on {multi} worker(s)")
        if dask_scheduler:
            concurrency = "dask"
        elif tiles_count == 1 or multi == 1 or multi is None:
            concurrency = None
        else:
            concurrency = "processes"
        return mapchete.Job(
            _msg_wrapper,
            fargs=(
                msg_callback,
                mp,
            ),
            fkwargs=dict(
                tile=tile,
                multi=multi,
                zoom=None if tile else zoom,
            ),
            executor_concurrency=concurrency,
            executor_kwargs=dict(
                dask_scheduler=dask_scheduler,
                max_chunksize=max_chunksize,
                multiprocessing_start_method=multiprocessing_start_method,
            ),
            as_iterator=as_iterator,
            total=1 if tile else tiles_count,
        )
    # explicitly exit the mp object on failure
    except Exception:  # pragma: no cover
        mp.__exit__(None, None, None)
        raise


def _msg_wrapper(msg_callback, mp, executor=None, **kwargs):
    try:
        for process_info in mp.batch_processor(executor=executor, **kwargs):
            yield process_info
            msg_callback(
                f"Tile {process_info.tile.id}: {process_info.process_msg}, {process_info.write_msg}"
            )
    # explicitly exit the mp object on success
    finally:
        mp.__exit__(None, None, None)

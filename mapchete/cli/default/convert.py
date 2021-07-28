import click
from rasterio.dtypes import dtype_ranges
from rasterio.enums import Resampling
from rasterio.rio.options import creation_options
import tilematrix
import tqdm

import mapchete
from mapchete import commands
from mapchete.cli import utils
from mapchete.formats import available_output_formats

OUTPUT_FORMATS = available_output_formats()


def _validate_bidx(ctx, param, bidx):
    if bidx:
        try:
            return list(map(int, bidx.split(",")))
        except ValueError:
            raise click.BadParameter("band indexes must be positive integer values")


@click.command(help="Convert outputs or other geodata.")
@utils.arg_tiledir
@utils.arg_output
@utils.opt_zoom
@utils.opt_bounds
@utils.opt_bounds_crs
@utils.opt_area
@utils.opt_area_crs
@utils.opt_point
@utils.opt_point_crs
@click.option(
    "--clip-geometry",
    "-c",
    type=click.Path(exists=True),
    help="Clip output by geometry.",
)
@click.option("--bidx", callback=_validate_bidx, help="Band indexes to copy.")
@click.option(
    "--output-pyramid",
    type=click.Choice(tilematrix._conf.PYRAMID_PARAMS.keys()),
    help="Output pyramid to write to.",
)
@click.option(
    "--output-metatiling",
    type=click.INT,
    help="Output metatiling.",
)
@click.option(
    "--output-format",
    type=click.Choice(OUTPUT_FORMATS),
    help="Output format.",
)
@click.option(
    "--output-dtype",
    type=click.Choice(dtype_ranges.keys()),
    help="Output data type (for raster output only).",
)
@click.option(
    "--output-geometry-type",
    type=click.STRING,
    help="Output geometry type (for vector output only).",
)
@creation_options
@click.option(
    "--scale-ratio",
    type=click.FLOAT,
    default=1.0,
    help="Scaling factor (for raster output only).",
)
@click.option(
    "--scale-offset",
    type=click.FLOAT,
    default=0.0,
    help="Scaling offset (for raster output only).",
)
@utils.opt_resampling_method
@click.option(
    "--overviews", is_flag=True, help="Generate overviews (single GTiff output only)."
)
@click.option(
    "--overviews-resampling-method",
    type=click.Choice([it.name for it in Resampling if it.value in range(8)]),
    default="cubic_spline",
    help="Resampling method used for overviews. (default: cubic_spline)",
)
@click.option(
    "--cog",
    is_flag=True,
    help="Write a valid COG. This will automatically generate verviews. (GTiff only)",
)
@utils.opt_overwrite
@utils.opt_verbose
@utils.opt_no_pbar
@utils.opt_debug
@utils.opt_multi
@utils.opt_concurrency
@utils.opt_logfile
@utils.opt_vrt
@utils.opt_idx_out_dir
def convert(
    tiledir,
    output,
    *args,
    vrt=False,
    idx_out_dir=None,
    debug=False,
    no_pbar=False,
    verbose=False,
    logfile=None,
    **kwargs,
):
    with mapchete.Timer() as t:
        job = commands.convert(
            tiledir,
            output,
            *args,
            as_iterator=True,
            msg_callback=tqdm.tqdm.write if verbose else None,
            **kwargs,
        )
        if not len(job):
            return
        list(
            tqdm.tqdm(
                job,
                unit="tile",
                disable=debug or no_pbar,
            )
        )
        tqdm.tqdm.write(f"processing {tiledir} finished in {t}")

    if vrt:
        tqdm.tqdm.write("creating VRT(s)")
        list(
            tqdm.tqdm(
                commands.index(
                    output,
                    *args,
                    vrt=vrt,
                    idx_out_dir=idx_out_dir,
                    as_iterator=True,
                    msg_callback=tqdm.tqdm.write if verbose else None,
                    **kwargs,
                ),
                unit="tile",
                disable=debug or no_pbar,
            )
        )
        tqdm.tqdm.write(f"index(es) creation for {tiledir} finished")

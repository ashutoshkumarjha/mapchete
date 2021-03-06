#########
Changelog
#########


-----------------
0.43 - 2021-09-17
-----------------

* core

  * `mapchete.io.vector.reproject_geometry()`:

    * use `pyproj` to determine CRS bounds to clip geometries when reprojecting
    * enable geometry segmentation before geometry is clipped (`segmentize_on_clip=False` and `segmentize_fraction=100` args)
  * suppress `rasterio` warnings when reading rasters (too many `rasterio.errors.NodataShadowWarning`s)

* packaging

  * add `pyproj` to dependencies


-----------------
0.42 - 2021-08-27
-----------------

* core

  * add option for input drivers to let processing-heavy tasks be handled by ``mapchete.Executor`` by implementing ``InputData.add_preprocessing_task()`` and ``InputData.get_preprocessing_task_result()`` methods
  * check futures submitted to ``mapchete.Executor`` for exceptions before yielding
  * remove deprecated ``multi`` (now called ``workers``), ``distributed`` and ``max_chunksize`` arguments

* CLI

  * remove deprecated ``--max-chunksize`` option
  * replace "tiles" with "tasks" in progress


-----------------
0.41 - 2021-08-17
-----------------

* core

  * add ``mapchete.commands`` package
  * add ``dask`` as optional ``Executor``
  * expose futures in ``Executor`` class to facilitate job cancellation
  * use ``spawn`` as default multiprocessing start method (#351)
  * fix missing worker logs (#185)
  * rename ``mapchete.cli.utils`` to ``mapchete.cli.options``
  * enable providing process code from within process config

* packaging

  * updated API doc

* CLI

  * CLI: change ``--multi`` option to ``--worker``
  * enable optional concurrency for ``mapchete cp``


-----------------
0.40 - 2021-06-24
-----------------

* core

  * fix overviews creation in sinlge GTiff output (#325)

* packaging

  * drop Python 3.6 support


-----------------
0.39 - 2021-06-08
-----------------

* core

  * fix warnings by removing deprecated calls (#336)
  * fix tiles count (#334)
  * default drivers

    * GTiff

      * pass on custom creation options to GTiff output driver / rasterio (#328)
      * change default GTiff profile (#335, #332)

        * compression: deflate
        * predictor: 2
        * blocksize: 512

    * GeoJSON

      * add LineString geometry type to available output schema (#338)

    * FlatGeobuf

      * add tiled FlatGeobuf output driver (#321)

  * CLI

    * ``cp`` and ``rm``

      * add fsspec filesystem creation options ``--src-fs-opts``, ``--dst-fs-opts`` and ``--fs-opts`` (#339)

  * default processes

    * ``convert``

      * print user warning if deprecated input name is used (#340)

* packaging

  * add black & flake8 code formatting tools (#337)


-----------------
0.38 - 2020-12-10
-----------------

* core

  * allow multipart geometries in GeoJSON (#300)
  * add ``Geobuf`` output format as alternative to store vector data (#302)
  * CLI:

    * ``convert``

      * enable converting vector data (#302)
      * add ``--output-geometry-type`` option for vector data output (#302)
      * fix omission of ``--output-metatiling`` (#302)

    * add ``rm`` command  (#306)

  * add ``mapchete.formats.driver_metadata()`` (#302)
  * add ``mapchete.formats.data_type_from_extension()`` (#302)
  * enable guessing data type (raster or vector) when reading from Tile Directories (#302)
  * ``mapchete.io.clean_geometry_type()``: add ``raise_exception`` flag to disable raising and returning an empty geometry instead (#302)
  * fix issue with ``rasterio>1.1.4`` (fix tile_to_zoom_level()) (#308)

* packaging

  * don't parse requirements.txt in setup.py (#301)
  * add test requirements (#302)


-----------------
0.37 - 2020-11-25
-----------------

* core

  * make retry settings configurable via environment (#296)

    * MAPCHETE_IO_RETRY_TRIES (default: 3)
    * MAPCHETE_IO_RETRY_DELAY (default: 1)
    * MAPCHETE_IO_RETRY_BACKOFF (default: 1)

  * fix non-overlapping bounds if provided as extra kwarg (#295)
  * don't pass on init bounds to mapchete input (#295)


-----------------
0.36 - 2020-11-24
-----------------

* core

  * create local output directory for single GTiff output files (#285)
  * add process area parameter (#287)
  * use optimized GDAL settings for baselayer creation (#291)
  * raise generic MapcheteIOError on read fails (#292)

* CLI

  * add more baselayers in ``serve`` (#278)
  * add ``cp`` command (#282)
  * enable ``serve`` to host multiple mapchete files (#289)
  * enable ``index`` to accept tile directories (#290)
  * expose multiprocessing start method as option in ``execute`` (#293)


-----------------
0.35 - 2020-08-04
-----------------
* fix index updates on remote TileDirectories (#274)
* pass on chunksize to multiprocessing & use ``Pool.__exit__()`` to close (#276)
* use GitHub actions instead of Travis CI
* update Fiona dependency to ``1.8.13.post1``


-----------------
0.34 - 2020-07-08
-----------------
* speed up extension loading by using ``importlib-metadata`` and ``importlib-resources`` instead of ``pkg_resources`` (#267)
* use ``boto`` paging to reduce requests to S3 bucket (#268)


-----------------
0.33 - 2020-03-24
-----------------
* use init_bounds instead of pyramid bounds on readonly mode (#257)
* clean up log messages (fix #251)


-----------------
0.32 - 2020-02-24
-----------------
* default process bounds are now bounds of the process pyramid instead of union of inputs (#242)
* fix overview pixelbuffer error at Antimeridian (#241)
* increased rasterio dependency to version ``1.0.28``
* add hillshade and contour extraction to registered default processes (#237)
* enable ``bigtiff`` and ``cog`` settings for single GTiff outputs (#247)
* enable ``--cog`` option for ``mapchete convert`` (#247)
* enable ``--bidx`` option (band subset) for ``mapchete convert`` (#248)
* only initialize inputs if necessary (#242)
* use ``rio-cogeo`` logic to determine whether to use a memory dataset or a temp file when writing a single GTiff (#217)


-----------------
0.31 - 2019-12-03
-----------------
* don't raise exception when one of the registered processes cannot be imported (#225)
* don't close pool between zoom levels (#227)
* ``_validate`` module renamed to ``validate`` (#230)
* fix inverted hillshade & misleading tile reference (#229)
* fix custom nodata values in overviews (#235)


-----------------
0.30 - 2019-10-22
-----------------
* fixed raise of ``FileNotFounderror`` on ``mapchete.io.raster.read_raster_no_crs()``
* fixed overview ``get_parent()`` on zoom 0 in batch processing
* sort processes alphabetically in ``mapchete processes``
* always raise ``FileNotFoundError`` if input file does not exist
* wait for 1 second between retry attempts on file read error
* added ``--overviews`` and ``--overviews-resampling-method`` to ``mapchete convert``
* fixed overview generation when output pixelbuffer was provided (#220)
* remote reading fixes (#219)
  * add GDAL HTTP options
  * handle ``AccessDenied`` exception which could occur if after an ``RasterioIOError`` a check is run if the file even exists
* increased required minimum NumPy version to 1.16
* pass on output parameters to mapchete process (#215, fixes #214)


-----------------
0.29 - 2019-07-12
-----------------
* fixed convert on single remote files (#205)
* fixed ``FileNotFoundError`` on ``driver_from_file()`` (#201)
* fixed zoom level order when processing multiple zooms (#207)
* inputs get intialized as readonly if only overviews are built (#140)
* AWS secrets get obfuscated in logs (#203)


-----------------
0.28 - 2019-06-18
-----------------

* breaking changes

  * output drivers must now provide ``OutputDataWriter`` and ``OutputDataReader`` classes instead of a single ``OutputData`` class
  * ``OutputDataWriter.close()`` method must accept ``exc_type=None, exc_value=None, exc_traceback=None`` keywords
  * ``mapchete pyramid`` CLI was removed and is replaced by the more versatile ``mapchete convert`` (#157, #192)
  * all CLI multiword options are separated by an hyphen (``-``) instead of underscore (``_``) (#189)

* overview tiles get also updated if child baselevel tile changes (#179)
* on ``batch_process()`` check which process output exists and only use parallelization for process tiles which will be processed (#179)
* fixed ``area_at_zoom()`` when using input groups (#181)
* fixed single GeoTIFF output bounds should use process area (#182)
* fixed YAML warning (#167)
* inputs preserve order (#176)
* enabled writing into single GeoTIFF files (#175)
* enabled multiprocessing spawn method (#173)
* extracted ``execute()`` logic to ``TileProcess`` class (#173)
* process workers now only receive objects and parameters they need (#173)
* parsing mapchete input does not fail if zoom levels do not match
* enable other projections again for GeoJSON output (closing #151)
* let rasterio & fiona decide whether single file can be opened (#186)
* provide option to show less content on CLI mapchete processes (#165)
* automatically detect loggers from registered mapchete packages and user process files
* enable drivers which do not handle pure NumPy arrays or feature lists
* ``OutputData`` classes have new ``output_valid()``, ``output_cleaned()`` and ``extract_subset()`` methods
* ``copy=False`` flag has been added to all NumPy ``.astype()`` calls to avoid unnecessary copying of arrays in memory
* extra requirements have been removed from ``requirements.txt``
* setup.py uses now ``find_packages()`` function to detect subpackages
* minimum required NumPy version is now 1.15


-----------------
0.27 - 2019-01-03
-----------------

* enable reading from output tile directories which have a different CRS
* enable GeoPackage as single file input
* fixed antimeridian shift check
* added retry decorator to read functions & added ``get_gdal_options()`` and
  ``read_raster_no_crs()`` functions
* pass on ``antimeridian_cutting`` from ``reproject_geometry()`` to underlying Fiona
  function
* fix transform shape on non-square tiles (#145)
* fixed VRT NODATA property, use GDAL typenames
* ``mapchete index`` shows progress bar for all tiles instead per zoom level and takes
  ``--point`` parameter
* tile directories now requires ``resampling`` in ``open()``, not in ``read()``
* added ``mapchete.processes.convert``
* use WKT CRS when writing VRT (closing #148)
* updated license year
* ``clean_geometry_type()`` raises ``GeometryTypeError`` if types do not match instead of
  returning ``None``
* default log level now is ``logging.WARNING``, not ``logging.ERROR``


-----------------
0.26 - 2018-11-27
-----------------

* enable VRT creation for indexes
* added ``--vrt`` flag and ``--idx_out_dir`` option to ``mapchete execute``
* renamed ``--out_dir`` to ``--idx_out_dir`` for ``mapchete index``
* ``BufferedTile`` shape (``height``, ``width``) and bounds (``left``, ``bottom``,
  ``right`` and ``top``) properties now return correct values
* ``BufferedTile.shape`` now follows the order ``(height, width)`` (update from
  ``tilematrix 0.18``)
* ``ReferencedRaster`` now also has a ``bounds`` property, take caution when unpacking
  results of ``create_mosaic()``!
* ``create_mosaic()``: use tile columns instead of tile bounding box union to determine
  whether tiles are passing the Antimeridian; fixes #141


-----------------
0.25 - 2018-10-29
-----------------

* use ``concurrent.futures`` instead of ``multiprocessing``
* make some dependencies optional (Flask, boto3, etc.)
* speed up ``count_tiles()``
* ``execute()`` function does not require explicit ``**kwargs`` anymore


-----------------
0.24 - 2018-10-23
-----------------

* breaking changes:

  * all Python versions < 3.5 are not supported anymore!

* default drivers now can handle S3 bucket outputs
* file based output drivers write output metadata into ``metadata.json``
* output directories can be used as input for other processes if they have a
  ``metadata.json``
* if Fiona driver has 'append' mode enabled, index entries get appended instead of writing
  a whole new file


-----------------
0.23 - 2018-08-21
-----------------

* breaking change:

  * for CLI utilities when providing minimum and maximum zoom, it has to have the form of
    ``5,6`` instead of ``5 6``

* remove deprecated ``memoryfile`` usage for ``write_raster_window()``
* fix ``s3`` path for ``mapchete index``
* add ``snap_bounds``, ``clip_bounds`` functions & ``effective_bounds`` to config
* made user processes importable as modules (#115)
* changed ``process_file`` paremeter to ``process``
* added ``mapchete.processes`` entry point to allow other packages add their processes
* switched from argparse to click
* ``execute`` and ``index`` commands accept now more than one mapchete files
* added ``mapchete.cli.commands`` entry point to allow other packages have ``mapchete``
  subcommands


-----------------
0.22 - 2018-05-31
-----------------

* don't pass on ``mapchete_file`` to ``execute()`` kwargs
* apply workaround for tqdm: https://github.com/tqdm/tqdm/issues/481


-----------------
0.21 - 2018-05-30
-----------------

* breaking change:

  * old-style Process classes are not supported anymore

* user process accepts kwargs from custom process parameters
* process_file is imported once when initializing the process (#114)
* when validating, import process_file to quickly reveal ``ImporError``
* fixed ``execute --point``
* also check for ``s3`` URLs when adding GDAL HTTP options
* default ``max_chunksize`` to 1 (#113)


-----------------
0.20 - 2018-04-07
-----------------

* fixed geometry reprojection for LineString and MultiLineString geometries (use buffer
  buffer to repair geometries does not work for these types)
* added ``RasterWindowMemoryFile()`` context manager around ``rasterio.io.MemoryFile``
  (#105)
* passing on dictionary together with numpy array from user process will write the
  dictionary as GeoTIFF tag (#101)
* added ``--wkt_geometry`` to ``execute`` which enables providing process bounds via WKT
* added ``--point`` to ``execute`` which enables providing a point location to be
  processed
* added ``--no_pbar`` to ``execute`` to disable progress bar
* ``mapchete index`` command now can create vector index files (``GeoJSON`` and
  ``GeoPackage``) and a text file containing output tile paths
* ``output.tiles_exist()`` now has two keyword arguments ``process_tile`` and
  ``output_tile`` to enable check for both tile types
* restructuring internal modules (core and config), no API changes


-----------------
0.19 - 2018-02-16
-----------------

* made logging functionality now library friendly (#102)
* added ``mapchete.log`` module with functions simplifying logging for user processes and
  driver plugins
* ``mapchete execute``

  * ``--logfile`` flag writes log files with debug level
  * ``--debug`` disables progress bar & prints debug log output
  * ``--verbose`` enables printing of process tile information while showing the
    progress bar
  * ``--max_chunksize`` lets user decide which maximum chunk size is used by
    ``multiprocessing``

* batch processing module

  * ``mapchete._batch`` functionality absorbed into main module
  * writing output is now handled by workers instead by main process
  * new function ``Mapchete.batch_processor()`` is a generator which processes all of
    the process tiles and returns information (i.e. processing & write times)
  * ``Mapchete.batch_process()`` consumes ``Mapchete.batch_processor()`` without
    returning anything
  * ``quiet`` and ``debug`` flags are deprecated and removed

* ``get_segmentize_value()`` moved from ``mapchete.formats.defaults.raster_file`` to
  ``mapchete.io``
* use GDAL options for remote files (closing #103) per default:

  * ``GDAL_DISABLE_READDIR_ON_OPEN=True``
  * ``GDAL_HTTP_TIMEOUT=30``

* introduced ``mapchete.io.path_is_remote()``


-----------------
0.18 - 2018-02-02
-----------------

* verstion 0.17 was not properly deployed, therefore nev version


-----------------
0.17 - 2018-02-02
-----------------

* ``write_raster_window`` now returns a ``rasterio.MemoryFile()`` if path is
  ``"memoryfile"``
* refactoring of ``MapcheteConfig`` (#99):

  * mapchete configuration changes:

    * ``process_zoom`` and ``process_minzoom``, ``process_maxzoom`` now have to be set via
      ``zoom_levels`` parameter
    * process pyramid now has to be set via a ``pyramid`` dictionary at root element (#78)
    * pyramid type is now called ``grid`` instead of ``type``
    * tile pyramids can now have custom grids (see
      https://github.com/ungarj/tilematrix/blob/master/doc/tilematrix.md#tilepyramid)
    * ``process_bounds`` are now called ``bounds``

  * API changes:

    * new attributes:

      * ``init_zoom_levels`` is a subset of ``zoom_levels`` and indicates initialization
        zoom levels via the ``zoom`` kwarg
      * ``init_bounds`` is a subset of ``bounds`` and indicates initialization bounds via
        the ``bounds`` kwarg

    * deprecated attributes:

      * ``crs`` is now found at ``process_pyramid.crs``
      * ``metatiling`` is now found at ``process_pyramid.metatiling``
      * ``pixelbuffer`` is now found at ``process_pyramid.pixelbuffer``
      * ``inputs`` was renamed to ``input``
      * ``process_bounds`` was renamed to ``bounds``

    * deprecated methods:

      * ``at_zoom()`` now called ``params_at_zoom()``
      * ``process_area()`` now called ``area_at_zoom()``
      * ``process_bounds()`` now called ``bounds_at_zoom()``


-----------------
0.16 - 2018-01-12
-----------------

* added ``TileDirectory`` as additional input option (#89)
* make all default output formats available in ``serve`` (#63)
* remove Pillow from dependencies (related to #63)


-----------------
0.15 - 2018-01-02
-----------------

* enabled optional ``cleanup()`` function for ``InputData`` objects when ``Mapchete`` is
  closed.


-----------------
0.14 - 2018-01-02
-----------------

* added python 3.4, 3.5 and 3.6 support


-----------------
0.13 - 2017-12-21
-----------------

* driver using ``InputData`` function must now accept ``**kwargs``
* fixed ``resampling`` issue introduced with inapropriate usage of ``WarpedVRT`` in
  ``read_raster_window()``
* ``str`` checks now use ``basestring`` to also cover ``unicode`` encodings
* ``read_raster_window()`` now accepts GDAL options which get passed on to
  ``rasterio.Env()``
* all resampling methods from ``rasterio.enums.Resampling`` are now available (#88)


-----------------
0.12 - 2017-11-23
-----------------

* adapt chunksize formula to limit ``multiprocessing`` chunksize between 0 and 16; this
  resolves occuring ``MemoryError()`` and some performance impediments, closing #82
* GeoTIFF output driver: use ``compress`` (like in rasterio) instead of ``compression`` &
  raise ``DeprecationWarning`` when latter is used


-----------------
0.11 - 2017-11-09
-----------------

* ``vector.reproject_geometry()`` throws now ``shapely.errors.TopologicalError`` instead
  of ``RuntimeError`` if reprojected geometry is invalid
* ``vector.reproject_geometry()`` now uses ``fiona.transform.transform_geom()`` internally
* pass on delimiters (zoom levels & process bounds) to drivers ``InputData`` object
* when a tile is specified in ``mapchete execute``, process bounds are clipped to tile
  bounds
* better estimate ``chunksize`` for multiprocessing in tile processing & preparing inputs
* add nodata argument to ``read_raster_window()`` to fix ``rasterio.vrt.WarpedVRT``
  resampling issue


-----------------
0.10 - 2017-10-23
-----------------

* better memory handling by detatching process output data from ``BufferedTile`` objects
* breaking API changes:

  * ``Mapchete.execute()`` returns raw data instead of tile with data attribute
  * ``Mapchete.read()`` returns raw data instead of tile with data attribute
  * ``Mapchete.get_raw_output()`` returns raw data instead of tile with data attribute
  * ``Mapchete.write()`` requires process_tile and data as arguments
  * same valid for all other ``read()`` and ``write()`` functions in drivers &
    ``MapcheteProcess`` object
  * formats ``is_empty()`` function makes just a basic intersection check but does not
    actually look into the data anymore
  * formats ``read()`` functions are not generators anymore but follow the rasterio style
    (2D array when one band index is given, 3D arrays for multiple band indices)

* new ``MapcheteNodataTile`` exception to indicate an empty process output
* raster_file & geotiff Input cache removed
* ``get_segmentize_value()`` function is now public
* use ``rasterio.vrt.WarpedVRT`` class to read raster windows
* source rasters without nodata value or mask are now handled properly (previously a
  default nodata value of 0 was assumed)


----------------
0.9 - 2017-10-04
----------------

* removed GDAL from dependencies by reimplementing ogr ``segmentize()`` using shapely
* use ``cascaded_union()`` instead of ``MultiPolygon`` to determine process area


----------------
0.8 - 2017-09-22
----------------

* process file now will accept a simple ``execute(mp)`` function
* current version number is now accessable at ``mapchete.__version`` (#77)
* added ``--version`` flag to command line tools


----------------
0.7 - 2017-09-20
----------------

* fixed PNG alpha band handling
* added generic ``MapcheteEmptyInputTile`` exception
* internal: available pyramid types are now loaded dynamically from ``tilematrix``
* closed #25: use HTTP errors instead of generating pink tiles in ``mapchete serve``


----------------
0.6 - 2017-09-08
----------------

* ``input_files`` config option now raises a deprecation warning and will be replaced with
  ``input``
* abstract ``input`` types are now available which is necessary for additional non-file
  based input drivers such as DB connections
* improved antimeridian handling in ``create_mosaic()`` (#69)
* improved baselevel generation performance (#74)


----------------
0.5 - 2017-05-07
----------------

* introduced iterable input data groups
* introduced pytest & test coverage of 92%
* adding Travis CI and coveralls integrations
* automated pypi deploy
* introduced ``mapchete.open()`` and ``batch_process()``
* progress bar on batch process
* proper logging & custom exceptions
* documentation on readthedocs.io


----------------
0.4 - 2017-03-02
----------------

* introduced pluggable format drivers (#47)
* ``mapchete formats`` subcommand added; lists available input & output formats
* completely refactored internal module structure
* removed ``self.write()`` function; process outputs now have to be passed on
  via ``return`` (#27)
* ``baselevel`` option now works for both upper and lower zoom levels
* added compression options for GTiff output
* make documentation and docstrings compatible for readthedocs.org


----------------
0.3 - 2016-09-20
----------------

* added new overall ``mapchete`` command line tool, which will replace
  ``mapchete_execute``, ``mapchete_serve`` and ``raster2pyramid``
* added ``mapchete create`` subcommand, which creates a dummy process
  (.mapchete & .py files)
* if using an input file from command line, the configuration input_file
  parameter must now be set to 'from_command_line' instead of 'cli'
* input files can now be opened directly using their identifier instead of
  self.params["input_files"]["identifier"]


----------------
0.2 - 2016-09-07
----------------

* fixed installation bug (io_utils module could not be found)
* rasterio's CRS() class now handles CRSes
* fixed tile --> metatile calculations
* fixed vector file read over antimeridian
* rewrote reproject_geometry() function


----------------
0.1 - 2016-08-23
----------------

* added vector data read
* added vector output (PostGIS & GeoJSON)
* added NumPy tile output
* added spherical mercator support
* tile with buffers next to antimeridian get full data
* combined output\_ ... parameters to output object in mapchete config files


-----
0.0.2
-----

* renamed ``mapchete_execute.py`` command to ``mapchete_execute``
* renamed ``mapchete_serve.py`` command to ``mapchete_serve``
* added ``raster2pyramid`` command
* added ``--tile`` flag in ``mapchete_execute`` for single tile processing
* added ``--port`` flag in ``mapchete_serve`` to customize port
* added ``clip_array_with_vector`` function for user-defined processes


-----
0.0.1
-----

* basic functionality of mapchete_execute
* parallel processing
* parsing of .mapchete files
* reading and writing of raster data

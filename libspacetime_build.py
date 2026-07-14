from cffi import FFI

ffibuilder = FFI()
ffibuilder.cdef(r"""
    // Manually imported header code. Cut out some comments and ifdefs.

    // Types
    typedef long mars_time_t;
    typedef long time_t;

    // Same as struct tm, but without timezones at the moment, and day is renamed to sol
    // Of course, the range of values will depend on Darian calendar
    struct mars_tm
    {
        int mars_tm_sec; /* Seconds, 0-59 (TODO: leap seconds?) */
        int mars_tm_min; /* Minutes, 0-59 */
        int mars_tm_hour; /* Hours, 0-23 */
        int mars_tm_msol; /* Sol of month, 1-28 */
        int mars_tm_mon; /* Month, 0-23 (TODO: Why start at 0 instead of 1 like for day?) */
        int mars_tm_year; /* Year, should be decent to just throw it in, as of writing the year is only 221. */
        int mars_tm_wsol; /* Sol of week, 0-6 */
        int mars_tm_ysol; /* Sol of year, 0-668 */

        long int mars_tm_amtoff; /* Seconds east of MTC. */
        const char* mars_tm_zone; /* Timezone abbreviation. */
    };

    mars_time_t mars_time(mars_time_t*);
    time_t mars_time_to_earth_time(mars_time_t);
    mars_time_t earth_time_to_mars_time(time_t);

    double diffmarstime(mars_time_t, mars_time_t);

    // (airy mean time instead of GMT)
    struct mars_tm* ammarstime(const mars_time_t*);

    mars_time_t mkmarstime(struct mars_tm*);

    size_t strfmarstime(char* restrict, size_t, const char* restrict, const struct mars_tm* restrict);
    char* strpmarstime(const char *restrict, const char *restrict, struct mars_tm *restrict);
    size_t wcsfmarstime(wchar_t *restrict, size_t, const wchar_t* restrict, const struct mars_tm* restrict);

    """)
ffibuilder.set_source("_libspacetime_cffi", """
    #include <time.h>
    #include <wchar.h>
    #include <libspacetime/mars.h>

    """, libraries=["spacetime"], include_dirs=["."])


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

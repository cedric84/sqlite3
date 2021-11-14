/**
 * @brief		The application entry point.
 * @file
 */

// https://sqlite.org/cintro.html

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <sqlite3.h>

/**
 * @brief		The entry point #0.
 */
static void
fct0(void)
{
	//---Check library version---//
	assert(SQLITE_VERSION_NUMBER	== sqlite3_libversion_number());

	//---Log the compilation options---//
	if (0) {
		for (int idx = 0; ; idx++) {
			//---Break the loop if there is no more compilation option---//
			const char*	opt	= sqlite3_compileoption_get(idx);
			if (NULL == opt) {
				break;
			}

			//---Log---//
			printf("%s\n", sqlite3_compileoption_get(idx));
		}
	}

	//---Open the database---//
	// https://sqlite.org/c3ref/sqlite3.html
	sqlite3*	db;
	assert(SQLITE_OK	== sqlite3_open("./test.db", &db));

	//---Create the statement---//
	// https://sqlite.org/c3ref/stmt.html
	sqlite3_stmt*	stmt;
	assert(SQLITE_OK	== sqlite3_prepare_v2(db, "SELECT * FROM pragma_compile_options()", -1, &stmt, NULL));

	//---Loop over each row---//
	const int	col_cnt	= sqlite3_column_count(stmt);
	for (int step_ret; SQLITE_DONE != (step_ret = sqlite3_step(stmt)); ) {
		//---Assert---//
		assert(SQLITE_ROW	== step_ret);

		//---Loop over each column---//
		for (int col_idx = 0; col_idx < col_cnt; col_idx++) {
			assert(SQLITE_TEXT	== sqlite3_column_type(stmt, col_idx));
			printf("%s ", sqlite3_column_text(stmt, col_idx));
		}
		printf("\n");
	}

	//---Release the statement---//
	assert(SQLITE_OK	== sqlite3_finalize(stmt));

	//---Release the database---//
	assert(SQLITE_OK	== sqlite3_close(db));
}

/**
 * @brief		The application entry point.
 * @param		[in]	argc	The number of arguments.
 * @param		[in]	argv	The arguments values.
 * @return		Returns EXIT_SUCCESS on success.
 */
extern int
main(int argc, char* argv[])
{
	printf("%s started\n", __func__);
	fct0();
	printf("%s terminated\n", __func__);
	return EXIT_SUCCESS;
}

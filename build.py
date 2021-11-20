import argparse
import pathlib
import os
import subprocess
import sys
import shutil

def run(*args):
	"""Runs the specified command."""
	ret = subprocess.Popen(args).wait()
	if (0 != ret):
		sys.exit(ret)

class host_t:
	"""The host class."""
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__()

		#---Zero---#
		self.install_pfx	= user_args.install_pfx.absolute()

	def autoreconf(self):
		"""Update generated configuration files."""
		run("autoreconf", "-f", "-i")

	def configure(self, triplet, *args):
		"""Configure the build."""
		install_pfx	= self.install_pfx.joinpath(triplet)
		run("./configure",
			"--prefix=" + str(install_pfx),
			"--enable-shared",
			"--enable-static",
			*args
		)

	def make(self):
		"""Runs the build."""
		run("make")

	def install(self):
		"""Installs the build."""
		run("make", "install")

	def clean(self):
		"""Cleans the build."""
		run("git", "clean", "-fd")

class host_clg_pandeb9_t(host_t):
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__(user_args)

	def build_all(self):
		"""Builds all the supported targets."""
		configure_arg_arr	= [
			[
				"x86_64-linux",
				"--with-pic=yes",
				"CFLAGS=-Wall -Werror",
				"LDFLAGS=-Wl,-rpath,\\$$ORIGIN/../lib",
				"LIBS=-lm",
			],
			[
				"i686-mingw32",
				"--host=i686-w64-mingw32",
				"CC=i686-w64-mingw32-gcc -static-libgcc",
				"CFLAGS=-Wall -Werror",
			],
			[
				"x86_64-mingw32",
				"--host=x86_64-w64-mingw32",
				"CC=x86_64-w64-mingw32-gcc",
				"CFLAGS=-Wall -Werror",
			],
		]
		for configure_idx in range(0, len(configure_arg_arr)):
			configure_arg	= configure_arg_arr[configure_idx]
			self.autoreconf()
			self.configure(*configure_arg)
			self.make()
			self.install()
			self.clean()

class host_clg_macos_t(host_t):
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__(user_args)

	def build_all(self):
		"""Builds all the supported targets."""
		configure_arg_arr	= [
			[
				"x86_64-macos",
				"--with-pic=yes",
				"CFLAGS=-Wall -Werror",
			],
		]
		for configure_idx in range(0, len(configure_arg_arr)):
			configure_arg	= configure_arg_arr[configure_idx]
			self.configure(*configure_arg)
			self.make()
			self.install()
			self.clean()

class host_clg_freebsd64_t(host_t):
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__(user_args)

	def build_all(self):
		"""Builds all the supported targets."""
		configure_arg_arr	= [
			[
				"x86_64-freebsd",
				"--with-pic=yes",
				"CFLAGS=-Wall -Werror",
				"LDFLAGS=-Wl,-rpath,\\$$ORIGIN/../lib",
				"LIBS=-lm",
			],
		]
		for configure_idx in range(0, len(configure_arg_arr)):
			configure_arg	= configure_arg_arr[configure_idx]
			self.autoreconf()
			self.configure(*configure_arg)
			self.make()
			self.install()
			self.clean()

class host_clg_junior_t(host_t):
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__(user_args)

	def build_all(self):
		"""Builds all the supported targets."""
		# see https://sqlite.org/howtocompile.html
		configure_arg_arr	= [
			[
				"i686-mingw32",
				str(pathlib.Path(os.environ["MINGW_HOME32"], "bin", "gcc.exe")),
			],
		]
		for configure_idx in range(0, len(configure_arg_arr)):
			#---Definitions---#
			triplet			= configure_arg_arr[configure_idx][0]
			CC				= configure_arg_arr[configure_idx][1]
			include_path	= self.install_pfx.joinpath(triplet, "include")
			bin_path		= self.install_pfx.joinpath(triplet, "bin")
			lib_path		= self.install_pfx.joinpath(triplet, "lib")

			#---Create directories---#
			os.makedirs(str(include_path), exist_ok=not False)
			os.makedirs(str(bin_path), exist_ok=not False)
			os.makedirs(str(lib_path), exist_ok=not False)

			#---Compile---#
			run(CC,
				"-static-libgcc",
				"-Wall",
				"-Werror",
				"-shared",
				"-Wl,--out-implib," + str(lib_path.joinpath("libsqlite3.dll.a")),
				"-DSQLITE_THREADSAFE=1",
				"-DSQLITE_ENABLE_MATH_FUNCTIONS",
				"-DSQLITE_ENABLE_FTS4",
				"-DSQLITE_ENABLE_FTS5",
				"-DSQLITE_ENABLE_JSON1",
				"-DSQLITE_ENABLE_RTREE",
				"-DSQLITE_ENABLE_GEOPOLY",
				"-o", str(bin_path.joinpath("sqlite3.dll")),
				"sqlite3.c"
			)

			#---Copy header file---#
			shutil.copyfile("sqlite3.h", str(include_path.joinpath("sqlite3.h")))

class host_github_linux_t(host_clg_pandeb9_t):
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__(user_args)

class host_github_macos_t(host_clg_macos_t):
	def __del__(self):
		"""The destructor."""
		pass

	def __init__(self, user_args):
		"""The main constructor."""
		#---Call parent constructor---#
		super().__init__(user_args)





#---Define the hosts---#
host_names	= {
	"clg-pandeb9"	: host_clg_pandeb9_t,
	"clg-macos"		: host_clg_macos_t,
	"clg-freebsd64"	: host_clg_freebsd64_t,
	"clg-junior"	: host_clg_junior_t,
	"github-linux"	: host_github_linux_t,
	"github-macos"	: host_github_macos_t,
}

#---Parse the command line---#
parser	= argparse.ArgumentParser()
parser.add_argument("host"
	, type			= str
	, choices		= host_names.keys()
	, help			= "the name of the host this script is running on."
)
parser.add_argument("--install_pfx"
	, type			= pathlib.Path
	, default		= pathlib.Path(".").resolve().joinpath("install")
	, help			= "the installation path."
)
user_args	= parser.parse_args()

#---Create the host---#
host	= host_names[user_args.host](user_args)

#---Build all---#
os.chdir(str(pathlib.Path(__file__).parent.joinpath("sqlite3")))
host.build_all()

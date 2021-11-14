import argparse
import pathlib
import os
import subprocess
import sys

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
				"i686-mingw",
				"--host=i686-w64-mingw32",
				"CC=i686-w64-mingw32-gcc",
				"CFLAGS=-Wall -Werror",
			],
			[
				"x86_64-mingw",
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

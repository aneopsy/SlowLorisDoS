from distutils.core import setup
setup(
    name="Slowloris",
    packages=['slowloris'],
    entry_points={"console_scripts": ["slowloris=slowloris.__main__:main"]},
    version="0.1.0",
    description="Low bandwidth DoS tool. Slowloris write in Python.",
    author="Paul THEIS",
    author_email="paultevatheis@gmail.com",
    url="https://github.com/aneopsy/SlowLorisDoS",
    keywords=["dos", "http", "slowloris"]
)

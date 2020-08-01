# import atexit
from setuptools import setup
# from setuptools.command.install import install

# def _post_install():
#     import reportinator.reconfig
#     reportinator.reconfig.main(first_install=True)
#     print('POST INSTALL')

# class new_install(install):
#     def __init__(self, *args, **kwargs):
#         super(new_install, self).__init__(*args, **kwargs)
#         atexit.register(_post_install)

setup(name='itsie',
      version='0.1',
      description='Discover Personal Websites by Crawling the Internet',
      url='http://github.com/nerdynewt/itsie',
      author='Vishnu Namboodiri K S',
      author_email='vishnu.nks@niser.ac.in',
      license='GPL v3.0',
      packages=['itsie'],
      # cmdclass={
      #     'install': new_install,
      #     },
      package_data={
          "itsie": ["data/*.txt", "data/*.bloom"],
          },
      entry_points={
          "console_scripts": [
              "itsie = itsie.main:main",
              ]
          },
      # install_requires=[
      #     'matplotlib',
      #     'numpy',
      #     'ruamel.yaml',
      #     'doi2bib',
      #     'pandas',
      #     'pyyaml',
      #     'configurator',
      #     ],
      include_package_data=True,
      zip_safe=False)


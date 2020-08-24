import setuptools
# parse_requirements() returns generator of pip.req.InstallRequirement objects

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setuptools.setup(
    install_requires=reqs
)
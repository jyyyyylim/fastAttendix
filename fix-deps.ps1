invoke-webrequest -uri https://bootstrap.pypa.io/get-pip.py -outfile get-pip.py
$env:PYTHONWARNINGS='ignore::UserWarning:setuptools.distutils_patch:26'
py .\get-pip.py
pip install requests

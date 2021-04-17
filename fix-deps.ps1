invoke-webrequest -uri https://bootstrap.pypa.io/get-pip.py -outfile get-pip.py
py .\get-pip.py
pip install requests
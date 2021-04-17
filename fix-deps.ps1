invoke-webrequest -uri https://files.pythonhosted.org/packages/6b/47/c14abc08432ab22dc18b9892252efaf005ab44066de871e72a38d6af464b/requests-2.25.1.tar.gz -outfile requests-2.25.1.tar.gz
new-item -path '.\requestssrc' -itemtype directory
tar -xzf requests-2.25.1.tar.gz -C requestssrc

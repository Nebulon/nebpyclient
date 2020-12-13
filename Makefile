#
# Copyright 2020 Nebulon, Inc.
# All Rights Reserved.
#
# DISCLAIMER: THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
# EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

# Makefile for Nebulon Python SDK

#
# Configuration for Sphinx documentation
#
SPHINXOPTS  =
SPHINXBUILD = sphinx-build
SPHINXSRC   = docs
SPHINXDST   = build

.PHONY: pip clean html publish

help:
	@echo "make [html|pip|publish|clean]"

html: clean
	$(SPHINXBUILD) -b html "$(SPHINXSRC)" "$(SPHINXDST)/html" $(SPHINXOPTS)

pip: clean
	python3 setup.py sdist bdist_wheel
	rm -rf build
	rm -rf nebpyclient.egg-info

publish: pip
	python3 -m twine upload dist/*

clean:
	rm -rf build
	rm -rf dist
	rm -rf nebpyclient.egg-info


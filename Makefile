DIST_VERSION ?= 7

NAME = leapp-supplements
VERSION = 1.0.0
SPEC_FILE = $(NAME).spec
RPMBUILD_DIR = $(HOME)/rpmbuild
TARBALL_PREFIX = $(NAME)-el$(DIST_VERSION)toel$$(($(DIST_VERSION) + 1))-$(VERSION)
TARBALL = $(TARBALL_PREFIX).tar.gz

.PHONY: all clean tarball rpmbuild

all: rpmbuild

rpmbuild: tarball
	rpmbuild -ba packaging/$(SPEC_FILE) \
		--define "_builddir `pwd`/packaging/BUILD" \
		--define "_rpmdir `pwd`/packaging/RPMS" \
		--define "_sourcedir `pwd`/packaging/SOURCES"  \
		--define "_srcrpmdir `pwd`/packaging/SRPMS" \
		--define "_buildrootdir `pwd`/packaging/BUILDROOT" \
		--define "rhel $(DIST_VERSION)" \
		--define "dist .el$(DIST_VERSION)"
	cp packaging/RPMS/*/*.rpm .
	cp packaging/SRPMS/*.rpm .

tarball: prepare
	git archive --format=tar.gz --prefix=$(TARBALL_PREFIX)/ -o $(TARBALL) HEAD
	mv $(TARBALL) packaging/SOURCES/

prepare: clean
	mkdir -p packaging/{BUILD,RPMS,SOURCES,SRPMS,BUILDROOT}

clean:
	rm -rf packaging/{BUILD,RPMS,SOURCES,SRPMS,BUILDROOT}
	rm -f *.rpm packaging/*tar.gz
	find . -name 'leapp.db' | grep "\.leapp/leapp.db" | xargs rm -f
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

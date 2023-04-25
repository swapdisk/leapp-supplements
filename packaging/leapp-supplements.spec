# Define Globals
%global leapp_datadir %{_datadir}/leapp-repository
%global repositorydir %{leapp_datadir}/repositories
%global custom_repositorydir %{leapp_datadir}/custom-repositories
%global supplementsdir %{repositorydir}/system_upgrade_supplements

%if 0%{?rhel} == 7
    %define rpm_name leapp-supplements-el7toel8
%endif
%if 0%{?rhel} == 8
    %define rpm_name leapp-supplements-el8toel9
%endif

# Define RPM Preamble
Name:           %{rpm_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Custom actors for the Leapp project

License:        MIT
URL:            https://github.com/oamg/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel} == 7
### RHEL 7 ###
BuildRequires:  python-devel

Requires:       leapp
Requires:       python2-leapp
# Dependency on leapp-repository
Requires:       leapp-upgrade-el7toel8
%endif

%if 0%{?rhel} == 8
### RHEL 8 ###
BuildRequires:  python3-devel

Requires:       leapp
Requires:       python3-leapp
# Dependency on leapp-repository
Requires:       leapp-upgrade-el8toel9
%endif

%description
Custom leapp actors for the in-place upgrade to the next major version
of the Red Hat Enterprise Linux system.

%prep
%setup -q

%build
# TODO: built .pyc files

%install
install -m 0755 -d %{buildroot}%{custom_repositorydir}
install -m 0755 -d %{buildroot}%{repositorydir}
install -m 0755 -d %{buildroot}%{supplementsdir}
install -m 0755 -d %{buildroot}%{_sysconfdir}/leapp/repos.d/
cp -r repos/system_upgrade_supplements/* %{buildroot}%{supplementsdir}

# Remove irrelevant repositories - We don't want to ship them for the particular RHEL version
%if 0%{?rhel} == 7
rm -rf %{buildroot}%{supplementsdir}/el8toel9
%endif
%if 0%{?rhel} == 8
rm -rf %{buildroot}%{supplementsdir}/el7toel8
%endif

# remove component/unit tests
rm -rf `find %{buildroot}%{supplementsdir} -name "tests" -type d`
find %{buildroot}%{repositorydir} -name "Makefile" -delete

for DIRECTORY in $(find  %{buildroot}%{repositorydir}/  -mindepth 1 -maxdepth 1 -type d);
do
    REPOSITORY=$(basename $DIRECTORY)
    echo "Enabling repository $REPOSITORY"
    ln -s  %{repositorydir}/$REPOSITORY  %{buildroot}%{_sysconfdir}/leapp/repos.d/$REPOSITORY
done;

%files
%dir %{custom_repositorydir}
%dir %{repositorydir}
%{supplementsdir}/*
%{_sysconfdir}/leapp/repos.d/*

%changelog
* Tue Apr 25 2023 Marek Filip <mafilip@redhat.com>
- Initial RPM packaging

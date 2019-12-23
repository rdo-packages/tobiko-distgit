# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service tobiko

%global common_desc \
This package contains Tobiko tests framework. \
Tobiko is an OpenStack testing framework focusing on areas mostly \
complementary to Tempest.

Name:       openstack-%{service}
Version:    XXX
Release:    XXX
Summary:    Tobiko testing framework
License:    ASL 2.0
URL:        https://opendev.org/x/tobiko/

Source0:    http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-testscenarios

%description
%{common_desc}

%package -n  python%{pyver}-%{service}
Summary: Tobiko testing framework
%{?python_provide:%python_provide python%{pyver}-%{service}}

%if %{pyver} == 2
Requires:   ansible >= 2.4.0
%else
Requires:   python3dist(ansible) >= 2.4.0
%endif
Requires:   python%{pyver}-fixtures >= 3.0.0
Requires:   python%{pyver}-keystoneauth1 >= 3.4.0
Requires:   python%{pyver}-jinja2 >= 2.8
Requires:   python%{pyver}-eventlet >= 0.20.1
Requires:   python%{pyver}-neutron-lib >= 1.25.0
Requires:   python%{pyver}-os-faults >= 0.1.18
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-paramiko >= 2.4.0
Requires:   python%{pyver}-pbr >= 4.0.0
Requires:   python%{pyver}-heatclient >= 1.5.0
Requires:   python%{pyver}-glanceclient >= 2.16.0
Requires:   python%{pyver}-neutronclient >= 6.7.0
Requires:   python%{pyver}-novaclient >= 9.1.0
Requires:   python%{pyver}-octaviaclient >= 1.9.0
Requires:   python%{pyver}-openstackclient >= 3.0.0
Requires:   python%{pyver}-stestr >= 2.0
Requires:   python%{pyver}-six  >= 1.10.0
Requires:   python%{pyver}-testtools >= 2.2.0
Requires:   python%{pyver}-netaddr >= 0.7.19

%description -n python%{pyver}-%{service}
This package contains Tobiko testing framework and test cases.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{service}.egg-info

%build
%{pyver_build}

%install
%{pyver_install}

%files -n python%{pyver}-%{service}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/*.egg-info
%{_bindir}/tobiko
%{_bindir}/tobiko-create
%{_bindir}/tobiko-delete
%{_bindir}/tobiko-fault
%{_bindir}/tobiko-fixture
%{_bindir}/tobiko-keystone-credentials
%{_bindir}/tobiko-list

%changelog
# REMOVEME: error caused by commit https://opendev.org/x/tobiko008c9fcca094f7b0b6575c337f40b8c51318c47e


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service tobiko

%global common_desc \
This package contains Tobiko tests framework. \
Tobiko is an OpenStack testing framework focusing on areas mostly \
complementary to Tempest.

Name:       openstack-%{service}
Version:    0.4.1
Release:    1%{?dist}
Summary:    Tobiko testing framework
License:    ASL 2.0
URL:        https://opendev.org/x/tobiko/

Source0:    http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-mock
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-testscenarios

%description
%{common_desc}

%package -n  python3-%{service}
Summary: Tobiko testing framework
%{?python_provide:%python_provide python3-%{service}}

Requires:   python3-fixtures >= 3.0.0
Requires:   python3-keystoneauth1 >= 4.3.0
Requires:   python3-jinja2 >= 2.10.1
Requires:   python3-eventlet >= 0.20.1
Requires:   python3-neutron-lib >= 2.7.0
Requires:   python3-oslo-config >= 2:8.4.0
Requires:   python3-oslo-log >= 4.4.0
Requires:   python3-paramiko >= 2.7.2
Requires:   python3-pbr >= 5.5.1
Requires:   python3-heatclient >= 2.3.0
Requires:   python3-glanceclient >= 3.2.2
Requires:   python3-neutronclient >= 7.2.1
Requires:   python3-novaclient >= 17.2.1
Requires:   python3-octaviaclient >= 2.2.0
Requires:   python3-openstackclient >= 5.4.0
Requires:   python3-stestr >= 2.0.0
Requires:   python3-six >= 1.15.0
Requires:   python3-testtools >= 2.3.0
Requires:   python3-netaddr >= 0.7.19
Requires:   python3-docker >= 4.2.1
Requires:   python3-junitxml >= 0.7

%description -n python3-%{service}
This package contains Tobiko testing framework and test cases.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{service}.egg-info

%build
%{py3_build}

%install
%{py3_install}

%files -n python3-%{service}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{service}
%{python3_sitelib}/*.egg-info
%{_bindir}/tobiko-fixture
%{_bindir}/tobiko-keystone-credentials

%changelog
* Fri Apr 02 2021 RDO <dev@lists.rdoproject.org> 0.4.1-1
- Update to 0.4.1


# REMOVEME: error caused by commit https://opendev.org/x/tobiko/commit/11a625d2153fc131ac2de2679646b2b3e69b9fa3

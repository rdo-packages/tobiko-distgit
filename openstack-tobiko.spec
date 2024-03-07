%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some runtime reqs from automatic generator
# TODO(jcapitao): package sshtunnel in RDO
%global excluded_reqs sshtunnel
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate pytest-html sphinx openstackdocstheme

%global repo_bootstrap 0

%global service tobiko

%global common_desc \
This package contains Tobiko tests framework. \
Tobiko is an OpenStack testing framework focusing on areas mostly \
complementary to Tempest.

Name:       openstack-%{service}
Version:    0.6.14
Release:    1%{?dist}
Summary:    Tobiko testing framework
License:    Apache-2.0
URL:        https://opendev.org/x/tobiko/

Source0:    http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description
%{common_desc}

%package -n  python3-%{service}
Summary: Tobiko testing framework

%description -n python3-%{service}
This package contains Tobiko testing framework and test cases.

%prep
%autosetup -n %{service}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i '/.*TOX_CONSTRAINTS.*/d' tox.ini
sed -i '/.*TOX_EXTRA_REQUIREMENTS.*/d' tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
# requirements-override-centos C9S is providing pytest-6.2.2 while package requires >= 6.2.5
sed -i "s/pytest>=.*/pytest/" test-requirements.txt

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Exclude some bad-known runtime reqs
for pkg in %{excluded_reqs}; do
  sed -i /^${pkg}.*/d requirements.txt
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

%check
# TODO(jcapitao): enable tests when sshtunnel is packaged in RDO.
# The test suite is failing when loading the files at the beginning
# so we cannot exclude the tests failing.
#%%tox -e %{default_toxenv}

%files -n python3-%{service}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{service}
%{python3_sitelib}/*.dist-info
%{_bindir}/tobiko-fixture
%{_bindir}/tobiko-keystone-credentials

%changelog
* Tue Sep 19 2023 RDO <dev@lists.rdoproject.org> 0.6.14-1
- Update to 0.6.14


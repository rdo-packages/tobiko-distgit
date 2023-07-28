%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate pytest pytest-html sshtunnel sphinx openstackdocstheme

%global repo_bootstrap 0

%global service tobiko

%global common_desc \
This package contains Tobiko tests framework. \
Tobiko is an OpenStack testing framework focusing on areas mostly \
complementary to Tempest.

Name:       openstack-%{service}
Version:    XXX
Release:    XXX
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

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

%check
%tox -e ${default_toxenv}

%files -n python3-%{service}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{service}
%{python3_sitelib}/*.dist-info
%{_bindir}/tobiko-fixture
%{_bindir}/tobiko-keystone-credentials

%changelog


#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		responses
Summary:	A utility for mocking out the Python Requests library
Summary(pl.UTF-8):	Narzędzie do podstawiania atrap biblioteki Python Requests
Name:		python-%{module}
# keep 0.17.x here for python2 support
Version:	0.17.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://github.com/getsentry/responses/releases
Source0:	https://github.com/getsentry/responses/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	7b94ef2851112c11c3bf75455e4ebeff
Patch0:		%{name}-py2.patch
URL:		https://github.com/getsentry/responses
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
%if %{with tests}
BuildRequires:	python-cookies
BuildRequires:	python-coverage >= 3.7.1
BuildRequires:	python-flake8
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 4.6
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-localserver
BuildRequires:	python-requests >= 2.0
BuildRequires:	python-urllib3 >= 1.25.10
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage >= 3.7.1
BuildRequires:	python3-flake8
BuildRequires:	python3-pytest >= 4.6
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-localserver
BuildRequires:	python3-requests >= 2.0
BuildRequires:	python3-urllib3 >= 1.25.10
BuildRequires:	python3-six
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A utility library for mocking out the requests Python library.

%description -l pl.UTF-8
Biblioteka narzędziowa do podstawiania atrap biblioteki Pythona
requests.

%package -n python3-%{module}
Summary:	A utility for mocking out the Python Requests library
Summary(pl.UTF-8):	Narzędzie do podstawiania atrap biblioteki Python Requests
Group:		Libraries/Python

%description -n python3-%{module}
A utility library for mocking out the requests Python library.

%description -n python3-%{module} -l pl.UTF-8
Biblioteka narzędziowa do podstawiania atrap biblioteki Pythona
requests.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_localserver.plugin" \
%{__python} -m pytest responses
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_localserver.plugin" \
%{__python3} -m pytest responses
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES README.rst
%{py_sitescriptdir}/responses
%{py_sitescriptdir}/responses-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES README.rst
%{py3_sitescriptdir}/responses
%{py3_sitescriptdir}/responses-%{version}-py*.egg-info
%endif

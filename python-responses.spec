# NOTE: skipping tests due to missing dependencies: python-pytest-localserver
#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		responses
%define		egg_name	responses
%define		pypi_name	responses
Summary:	A utility for mocking out the Python Requests library
Name:		python-%{pypi_name}
Version:	0.9.0
Release:	1
License:	Apache v2.0
Source0:	https://github.com/getsentry/responses/archive/%{version}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	70b7510b9bcd87046ba450b440b7543d
Group:		Libraries/Python
URL:		https://github.com/getsentry/responses
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
%if %{with tests}
BuildRequires:	python-cookies
BuildRequires:	python-coverage
BuildRequires:	python-flake8
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-requests
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cookies
BuildRequires:	python3-coverage
BuildRequires:	python3-flake8
BuildRequires:	python3-mock
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-requests
BuildRequires:	python3-six
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A utility library for mocking out the requests Python library.

%package -n python3-%{pypi_name}
Summary:	A utility for mocking out the Python Requests library
Group:		Libraries/Python

%description -n python3-%{pypi_name}
A utility library for mocking out the requests Python library.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/test_responses.py*
%endif

%if %{with python3}
%py3_install
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/test_responses.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/__pycache__/test_responses.*.pyc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%{py_sitescriptdir}/%{module}.py[co]
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst LICENSE
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.cpython-*.pyc
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

Name:           fnal-snow-python
Summary:        Python Scripts and libraries to interact with Service Now @ FNAL
Version:        0.9.0
Release:        0%{?dist}
#Packager:       Tim Skirvin <tskirvin@fnal.gov>
Group:          Applications/System
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}-%{release}.tar.gz
BuildArch:      noarch

Requires:       python python-iso8601 
# also pysnow, no rpm available for that yet
BuildRequires:  rsync
Vendor:         FNAL USCMS-T1
License:        BSD
URL:            http://www.fnal.gov/

%description
Installs scripts and tools that provide an interface to the Fermi Service
Now interface via the JSON API.

%prep

%setup -c -q -n %{name}-%{version}-%{release}

%build

%install
python setup.py install --prefix=${RPM_BUILD_ROOT}/usr

rsync -Crlpt ./usr ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man1
for i in `ls usr/bin`; do
    pod2man --section 1 --center="System Commands" usr/bin/${i} \
        > ${RPM_BUILD_ROOT}/usr/share/man/man1/${i}.1 ;
done

%clean
# Adding empty clean section per rpmlint.  In this particular case, there is
# nothing to clean up as there is no build process

%files
%defattr(-,root,root)
/usr/bin/*
/usr/share/man/man1/*
%{python_sitelib}/pyfnalsnow/*py*
%{python_sitelib}/*egg-info

%changelog
* Wed Feb  8 2017   Tim Skirvin <tskirvin@fnal.gov> 0.9.0-0
- initial .spec file

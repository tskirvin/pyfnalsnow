Name:           fnal-snow-python
Summary:        Python Scripts and libraries to interact with Service Now @ FNAL
Version:        1.4.2
Release:        0%{?dist}
Group:          Applications/System
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}-%{release}.tar.gz
BuildArch:      noarch

%if 0%{?rhel} == 8
Requires:       python3 python3-requests python3-PyYAML
# also pysnow and iso8601, no rpm available for that yet
BuildRequires:  python3 python3-setuptools python3-rpm-macros rsync perl-podlators
%else
Requires:       python36 python36-iso8601 python36-requests python36-PyYAML
# also pysnow, no rpm available for that yet
BuildRequires:  python36 python36-setuptools python3-rpm-macros rsync perl-podlators
%endif
Vendor:         ECF-SSI
License:        Artistic 2.0
URL:            http://www.fnal.gov/

%description
Installs scripts and tools that provide an interface to the Fermi Service
Now interface via the JSON API.

%prep

%setup -c -q -n %{name}-%{version}-%{release}

%build

%install
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man1
for i in `ls usr/bin`; do
    pod2man --section 1 --center="System Commands" usr/bin/${i} \
        > ${RPM_BUILD_ROOT}/usr/share/man/man1/${i}.1 ;
done

rsync -Crlpt ./usr ${RPM_BUILD_ROOT}

python3 setup.py install --prefix=${RPM_BUILD_ROOT}/usr \
    --single-version-externally-managed --record=installed_files

rm -rf ${RPM_BUILD_ROOT}/usr/bin/.mypy_cache

%clean
# Adding empty clean section per rpmlint.  In this particular case, there is
# nothing to clean up as there is no build process

%files
%defattr(-,root,root)
/usr/bin/*
/usr/share/man/man1/*
%{python3_sitelib}/pyfnalsnow/*.py*
%{python3_sitelib}/pyfnalsnow/__pycache__/*.pyc
%{python3_sitelib}/*egg-info

%changelog
* Tue Dec  1 2020   Tim Skirvin <tskirvin@fnal.gov> 1.4.2-0
- Incident.py + snow-incident-list - can now search by age (number of days
  since the ticket was created)

* Mon Nov 16 2020   Tim Skirvin <tskirvin@fnal.gov> 1.4.1-0
- RITM.py - tktIsResolved() now says "False" for work-in-progress tickets
- various Exceptions fixed

* Mon Apr 20 2020   Tim Skirvin <tskirvin@fnal.gov> 1.4.0-0
- updated to work with new SNOW (where it's not at service-now.com anymore) 
- bug fixes

* Thu Nov 14 2019   Tim Skirvin <tskirvin@fnal.gov> 1.3.2-0
- fixes to make requestor work better with user guest, and to handle
  errors a bit more gracefully

* Mon Aug 19 2019   Tim Skirvin <tskirvin@fnal.gov> 1.3.1-0
- RITM.py - tktPending() 'unresolved' search now includes pending

* Mon Aug 19 2019   Tim Skirvin <tskirvin@fnal.gov> 1.3.0-0
- python 3
- ran through the flake8 python linter, cleaned up to match

* Wed Mar 20 2019   Tim Skirvin <tskirvin@fnal.gov> 1.2.3-0
- moving the changelog to CHANGELOG.md going forwards
- generally re-working for distribution via pypi

* Wed Dec 05 2018   Tim Skirvin <tskirvin@fnal.gov> 1.2.2-0
- snow-tkt-resolve - adds a 'goal' state so that we can cancel incidents
  instead of just resolving them
- Incident.py - changes to match

* Wed Nov 21 2018   Tim Skirvin <tskirvin@fnal.gov> 1.2.1-0
- add 'caller' search to snow-incident-list
- snow-incident-list format changes - includes CI if available, some tweaking
- add 'ciById' and 'ciByName' to __init__.py
- Incident.py knows how to deal with CIs and caller searches

* Wed Oct 03 2018   Tim Skirvin <tskirvin@fnal.gov> 1.2.0-0
- wrote snow-tkt-pending and interfaces for RITM
- snow-ritm-resolve was merged into snow-tkt-resolve
- tested and confirmed that 'resolve' works for Incident + RITM
  (also, test suite)
- snow-incident-create
- fixed Incident reporting for resolutions
- many miscellaneous bug fixes

* Tue Oct 02 2018   Tim Skirvin <tskirvin@fnal.gov> 1.1.1-0
- adding 'snow-tkt-resolve' and interfaces for Incident + RITM
- various bug fixes

* Mon Apr 30 2018   Tim Skirvin <tskirvin@fnal.gov> 1.1.0-0
- now uses pysnow 0.7.4

* Wed Feb 07 2018   Tim Skirvin <tskirvin@fnal.gov> 1.0.2-0
- snow-ritm-create - don't add extra newlines to the body of the ritms

* Mon Feb 13 2017   Tim Skirvin <tskirvin@fnal.gov> 1.0.1-0
- snow-ritm-create - now uses a config file template for new entries; adds
  support for urgency, priority, and basic categorization
- __init__.py - better support for "empty" journal entries
- ticket.py - _FieldOrEmpty(tkt) for internal use, should make it easier
  to deal with unknown field values

* Fri Feb 10 2017   Tim Skirvin <tskirvin@fnal.gov> 1.0.0-0
- initial release, still missing resolve/reopen and incident-create

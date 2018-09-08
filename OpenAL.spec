#
# Conditional build:
%bcond_without	alsa		# ALSA backend
%bcond_without	jack		# JACK backend
%bcond_without	portaudio	# PortAudio backend
%bcond_without	pulseaudio	# PulseAudio backend
%bcond_without	gui		# alsoft-config GUI
%bcond_with	qt4		# Qt 4 instead of Qt 5 for GUI
#
Summary:	Open Audio Library
Summary(pl.UTF-8):	Otwarta Biblioteka Dźwięku
Name:		OpenAL
Version:	1.19.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://kcat.strangesoft.net/openal-releases/openal-soft-%{version}.tar.bz2
# Source0-md5:	1f59accf1a187384e155e82663aa3f9a
#URL:		http://kcat.strangesoft.net/openal.html
URL:		http://www.openal.org/
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	cmake >= 3.0.2
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	pkgconfig
%{?with_portaudio:BuildRequires:	portaudio-devel}
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with gui}
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4.8.0
BuildRequires:	QtGui-devel >= 4.8.0
BuildRequires:	qt4-build >= 4.8.0
%else
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	qt5-build >= 5
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl.UTF-8
OpenAL, otwarta biblioteka dźwięku, to połączony wysiłek w celu
stworzenia otwartego, niezależnego od producentów, międzyplatformowego
interfejsu projektowania aplikacji w części obsługi dźwięku.
Biblioteka adresowana jest do twórców aplikacji i użytkowników,
którzy wybierają przenośne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada już wsparcie wielu
dostarczycieli sprzętu i programistów.

%package devel
Summary:	Headers for OpenAL
Summary(pl.UTF-8):	Pliki nagłówkowe do OpenAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne przy budowaniu programów opartych na
OpenAL.

%package gui
Summary:	OpenAL configuration GUI
Summary(pl.UTF-8):	Graficzny interfejs do konfiguracji biblioteki OpenAL
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore >= 4.8.0
Requires:	QtGui >= 4.8.0

%description gui
OpenAL configuration GUI.

%description gui -l pl.UTF-8
Graficzny interfejs do konfiguracji biblioteki OpenAL.

%prep
%setup -q -n openal-soft-%{version}

%build
cd build
%cmake .. \
	%{!?with_alsa:-DALSOFT_BACKEND_ALSA=OFF} \
	%{!?with_jack:-DALSOFT_BACKEND_JACK=OFF} \
	%{!?with_portaudio:-DALSOFT_BACKEND_PORTAUDIO=OFF} \
	%{!?with_pulseaudio:-DALSOFT_BACKEND_PULSEAUDIO=OFF} \
	-DALSOFT_EXAMPLES=OFF \
	%{!?with_gui:-DALSOFT_NO_CONFIG_UTIL=ON} \
	%{?with_qt4:-DALSOFT_NO_QT5=ON} \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/openal

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -p alsoftrc.sample $RPM_BUILD_ROOT%{_sysconfdir}/openal/alsoft.conf

# these look not really useful
%{__rm} $RPM_BUILD_ROOT%{_bindir}/altonegen

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openal
%attr(755,root,root) %{_bindir}/makehrtf
%attr(755,root,root) %{_bindir}/openal-info
%attr(755,root,root) %{_libdir}/libopenal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenal.so.1
%{_datadir}/openal

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenal.so
%{_includedir}/AL
%{_pkgconfigdir}/openal.pc
%{_libdir}/cmake/OpenAL

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/alsoft-config
%endif

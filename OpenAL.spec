#
# Conditional build:
%bcond_without	alsa		# without ALSA support
%bcond_without	portaudio	# without PortAudio support
%bcond_without	pulseaudio	# without PulseAudio support
#
Summary:	Open Audio Library
Summary(pl.UTF-8):	Otwarta Biblioteka Dźwięku
Name:		OpenAL
Version:	1.13
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://kcat.strangesoft.net/openal-releases/openal-soft-%{version}.tar.bz2
# Source0-md5:	58b7d2809790c70681b825644c5f3614
#URL:		http://kcat.strangesoft.net/openal.html
URL:		http://www.openal.org/
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	cmake
%{?with_portaudio:BuildRequires:	portaudio-devel}
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
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

%prep
%setup -q -n openal-soft-%{version}

%build
%cmake . \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_VERBOSE_MAKEFILE=1 \
	-DLIB_INSTALL_DIR=%{_lib} \
	%{!?with_alsa:-DALSA=OFF} \
	%{!?with_portaudio:-DPORTAUDIO=OFF} \
	%{!?with_pulseaudio:-DPULSEAUDIO=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/openal-info
%attr(755,root,root) %{_libdir}/libopenal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenal.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenal.so
%{_includedir}/AL
%{_pkgconfigdir}/openal.pc

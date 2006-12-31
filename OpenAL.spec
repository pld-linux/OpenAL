#
# Conditional build:
#
%bcond_without	alsa	# without ALSA support
%bcond_with	arts	# with aRts support
%bcond_without	esd	# without esd support
%bcond_without	mmx	# don't use MMX
#
%ifnarch %{ix86} %{x8664}
%undefine	with_mmx
%endif
%ifarch i386 i486
%undefine	with_mmx
%endif
Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D¼wiêku
Name:		OpenAL
Version:	0.0.8
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://www.openal.org/openal_webstf/downloads/openal-%{version}.tar.gz
# Source0-md5:	641cf53761f35ee979f3e888614797a0
URL:		http://www.openal.org/
Patch0:		%{name}-alc.h.patch
BuildRequires:	SDL-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	autoconf >= 2.56
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel}
%if %{with mmx}
# MMX code triggers ICE in gcc 3.3.x
BuildRequires:	gcc >= 5:3.4.0
%endif
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
%ifarch %{ix86}
%{?with_mmx:BuildRequires:	nasm}
%endif
BuildRequires:	pkgconfig
BuildRequires:	smpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with mmx}
%define		specflags_ia32	-mmmx
%else
%define		specflags_ia32	-U__MMX__
%endif

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta biblioteka d¼wiêku, to po³±czony wysi³ek w celu
stworzenia otwartego, niezale¿nego od producentów, miêdzyplatformowego
interfejsu projektowania aplikacji w czê¶ci obs³ugi d¼wiêku.
Biblioteka adresowana jest do twórców aplikacji i u¿ytkowników,
którzy wybieraj± przeno¶ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada ju¿ wsparcie wielu
dostarczycieli sprzêtu i programistów.

%package devel
Summary:	Headers for OpenAL
Summary(pl):	Pliki nag³ówkowe do OpenAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag³ówkowe potrzebne przy budowaniu programów opartych na
OpenAL.

%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OpenAL static library.

%description static -l pl
Biblioteka OpenAL do konsolidacji statycznej.

%prep
%setup -q -n openal-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I admin/autotools/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?with_alsa:en}%{!?with_alsa:dis}able-alsa{,-dlopen} \
	--%{?with_arts:en}%{!?with_arts:dis}able-arts{,-dlopen} \
	--%{?with_esd:en}%{!?with_esd:dis}able-esd{,-dlopen} \
	--enable-sdl --enable-sdl-dlopen \
	--enable-capture \
	--enable-linux \
	--enable-null \
%ifarch amd64 x86_64 athlon i686 i586
	--enable-optim-generic \
%endif
	--enable-waveout \
	--enable-vorbis --enable-vorbis-dlopen \
	--enable-mp3 --enable-mp3-dlopen \
	--with-gcc="%{__cc}"

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
%doc ChangeLog NOTES TODO
%attr(755,root,root) %{_libdir}/libopenal.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc common/specification/OpenAL1-1Spec.pdf
%attr(755,root,root) %{_bindir}/openal-config
%attr(755,root,root) %{_libdir}/libopenal.so
%{_libdir}/libopenal.la
%{_includedir}/AL
%{_pkgconfigdir}/openal.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenal.a

Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D¼wiêku
Name:		OpenAL
Version:	0.0.6
Release:	1
License:	LGPL
Group:		X11/Libraries
Vendor:		Loki Entertainment Software - http://www.lokigames.com/
# This is tarball taken directly form Mandrake Cooker .src.rpm
Source0:	%{name}-linuxonly-20010805.tar.bz2
# Those patches came from Mandrake Cooker (only changed names)
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-build.patch
URL:		http://www.openal.com/
BuildRequires:	alsa-lib-devel
BuildRequires:	SDL-devel
BuildRequires:	libvorbis-devel
BuildRequires:	smpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta biblioteka d¼wiêku, to po³±czony wysi³ek w celu
stworzenia otwartego, niezale¿nego od producentów, miedzyplatformowego
interfejsu projektowania aplikacji w czê¶ci obs³ugi d¼wiêku.
Biblioteka adresowana jest do twórców aplikacji i u¿ytkowników,
którzy wybieraj± przeno¶ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada ju¿ wsparcie wielu
dostarczycieli sprzêtu i programistów.

%package devel
Summary:	Headers for OpenAL
Summary(pl):	Pliki nag³ówkowe do OpenAL
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag³ówkowe potrzebne przy budowaniu programów opartych na
OpenAL.

%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OpenAL static library.

%description static -l pl
Biblioteka OpenAL do statycznego linkowania.

%prep
%setup -q -n tmp/openal
%patch0 -p0
%patch1 -p0

%build
cd linux
sh ./autogen.sh
%configure  --enable-prefix=%{_prefix} \
            --enable-optimization \
	    --enable-alsa \
	    --enable-sdl \
	    --enable-vorbis \
	    --enable-smpeg \
	    --enable-capture \
	    --with-gcc=%{__cc}			    
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd linux
%makeinstall

mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -c  doc/openal.info $RPM_BUILD_ROOT%{_infodir}

# This needs patch, but is it worth to waste time ?
rm -f $RPM_BUILD_ROOT%{_libdir}/libopenal.{so,so.0}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun	devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1


%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so*

%files devel
%defattr(644,root,root,755)
%doc %{_infodir}/openal.info.*
%{_includedir}/AL/*.h

%files static
%defattr(644,root,root,755)
%attr(755,root,root)%{_libdir}/*.a

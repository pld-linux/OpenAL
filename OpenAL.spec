Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka DºwiÍku
Name:		OpenAL
Version:	0.0.6
Release:	1
License:	LGPL
Group:		X11/Libraries
Group(de):	X11/Libraries
Group(es):	X11/Bibliotecas
Group(fr):	X11/Librairies
Group(pl):	X11/Biblioteki
Group(pt_BR):	X11/Bibliotecas
Group(ru):	X11/‚…¬Ã…œ‘≈À…
Group(uk):	X11/‚¶¬Ã¶œ‘≈À…
Vendor:		Loki Entertainment Software - http://www.lokigames.com/
# This is tarball taken directly form Mandrake Cooker .src.rpm
Source0:	%{name}-linuxonly-20010805.tar.bz2
# Those patches came from Mandrake Cooker (only changed names)
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-build.patch
URL:		http://www.openal.com/
BuildRequires:  alsa-lib-devel
BuildRequires:  SDL-devel
BuildRequires:  libvorbis-devel
BuildRequires:  smpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6/

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta bibliotela dºwiÍku, to po≥±czony wysi≥ek w celu
stworzenia otwartego, niezaleønego od producentÛw, miedzyplatformowego
interfejsu projektowania aplikacji w czÍ∂ci obs≥ugi dºwiÍku.
Biblioteka adersowana jest do twÛrcÛw aplikacji i urzytkownikÛw,
ktÛrzy wybieraj± przeno∂ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada juø wsparcie wielu
dostarczycieli sprzÍtu i programistÛw.


%package devel
Summary:	Headers for OpenAL
Group:		Development
Group(de):	Entwicklung
Group(es):	Desarrollo
Group(pl):	Programowanie
Group(pt_BR):	Desenvolvimento
Group(ru):	Ú¡⁄“¡¬œ‘À¡
Group(uk):	Úœ⁄“œ¬À¡

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag≥Ûwkowe potrzebne przy budowaniu programÛw opartych na
OpenAL.


%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Building
Group(de):	Entwicklung/Bauen
Group(pl):	Programowanie/Budowanie

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
install -c  doc/openal.info $RPM_BUILD_ROOT/%{_infodir}

# This needs patch, but is it worth to waste time ?
rm -f $RPM_BUILD_ROOT%{_libdir}/libopenal.{so,so.0}


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so*

%files devel
%defattr(644,root,root,755)
%doc %{_infodir}/openal.info.*
%{_includedir}/AL/*.h


%files static
%defattr(644,root,root,755)
%attr(755,root,root)%{_libdir}/*.a*

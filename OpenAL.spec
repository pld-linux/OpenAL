Summary:	OpenAL - Open Audio Library
Summary(pl):	OpenAL - Otwarta Biblioteka DºwiÍku
Name:		OpenAL
Version:	20011116
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
Source0:	ftp://ftp.openal.com/nie-wiem-co-tu-daÊ.tar.bz2/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.openal.com/nie-wiem-co-tu-daÊ.tar.bz2/%{name}-headers-%{version}.tar.bz2
Patch0:		%{name}-stdio.patch
Patch1:		%{name}-include_unconsequency.patch
Patch2:		%{name}-symlinks.patch
URL:		http://www.openal.com/
BuildRequires:	alsa-lib-devel
BuildRequires:	SDL-devel
BuildRequires:	libvorbis-devel
BuildRequires:	smpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta biblioteka dºwiÍku, to po≥±czony wysi≥ek w celu
stworzenia otwartego, niezaleønego od producentÛw, miedzyplatformowego
interfejsu projektowania aplikacji w czÍ∂ci obs≥ugi dºwiÍku.
Biblioteka adresowana jest do twÛrcÛw aplikacji i uøytkownikÛw, ktÛrzy
wybieraj± przeno∂ne standardy, jak OpenGL, w grach i aplikacjach
multimedialnych. OpenAL posiada juø wsparcie wielu dostarczycieli
sprzÍtu i programistÛw.

%package devel
Summary:	OpenAL development files
Summary(pl):	Pakiet dla programistÛw OpenAL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}

%description devel
OpenAL header files.

%description devel -l pl
Pliki nag≥Ûwkowe biblioteki OpenAL.

%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}

%description static
OpenAL static library.

%description static -l pl
Biblioteka OpenAL do statycznego linkowania.

%prep
%setup -q -n %{name} -a 1
cp -f AL/*.h include/AL/
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./autogen.sh
./configure \
	--enable-prefix=%{_prefix} \
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
%{__make} install DESTDIR=$RPM_BUILD_ROOT%{_prefix}/
ln -sf libopenal.so.0.0.6 $RPM_BUILD_ROOT%{_libdir}/libopenal.so
gzip -9nf TODO NOTES ChangeLog CREDITS

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/AL
%attr(755,root,root) %{_libdir}/*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

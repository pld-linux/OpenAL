Summary:	OpenAL - Open Audio Library
Summary(pl):	OpenAL - Otwarta Biblioteka D¼wiêku
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
Group(ru):	X11/âÉÂÌÉÏÔÅËÉ
Group(uk):	X11/â¦ÂÌ¦ÏÔÅËÉ
Vendor:		Loki Entertainment Software - http://www.lokigames.com/
Source0:	ftp://ftp.openal.com/nie-wiem-co-tu-daæ.tar.bz2/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.openal.com/nie-wiem-co-tu-daæ.tar.bz2/%{name}-headers-%{version}.tar.bz2
Patch0:		%{name}-stdio.patch
Patch1:		%{name}-include_unconsequency.patch
Patch2:		%{name}-symlinks.patch
URL:		http://www.openal.com/
BuildRequires:	alsa-lib-devel
BuildRequires:	SDL-devel
BuildRequires:	libvorbis-devel
BuildRequires:	smpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
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
OpenAL, otwarta bibliotela d¼wiêku, to po³±czony wysi³ek w celu
stworzenia otwartego, niezale¿nego od producentów, miedzyplatformowego
interfejsu projektowania aplikacji w czê¶ci obs³ugi d¼wiêku.
Biblioteka adersowana jest do twórców aplikacji i urzytkowników,
którzy wybieraj± przeno¶ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada ju¿ wsparcie wielu
dostarczycieli sprzêtu i programistów.


%package devel
Summary:	OpenAL development files
Summary(pl):	Pakiet dla Programistów OpenAL
Group:		Development/Building
Group(de):	Entwicklung/Bauen
Group(pl):	Programowanie/Budowanie
Requires:	%{name} = %{version}

%description devel
OpenAL header files.

%description devel -l pl
Pliki nag³ówkowe biblioteki OpenAL.


%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Building
Group(de):	Entwicklung/Bauen
Group(pl):	Programowanie/Budowanie
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
CFLAGS="%{rpmcflags} -I%{_includedir} \
	-fexpensive-optimizations 	-funroll-all-loops \
	-funroll-loops 			-fomit-frame-pointer \
	-finline-functions 		-ffast-math "
export CFLAGS

LDFLAGS="-L%{_libdir}" ; export LDFLAGS

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
%{__make} install DESTDIR=$RPM_BUILD_ROOT/%{_prefix}

gzip -9nf TODO NOTES ChangeLog CREDITS COPYING

cd $RPM_BUILD_ROOT/%{_libdir}
ln -sf libopenal.so.0.0.6 libopenal.so.0
ln -sf libopenal.so.0.0.6 libopenal.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%{_libdir}/*so*

%files devel
%defattr(644,root,root,755)
%{_includedir}/AL/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

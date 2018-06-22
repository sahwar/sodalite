APPNAME=sodalite

#SHELL=${/usr/bin/sh}
INSTALL=install
INSTALL_PROGRAM=${INSTALL}
INSTALL_DATA=${INSTALL} -m 644

prefix=/usr/local
exec_prefix=${prefix}
bindir=${exec_prefix}/bin
datarootdir=${prefix}/share
datadir=${datarootdir}
appdatadir=${datadir}/${APPNAME}
sysconfdir=${prefix}/etc
localstatedir=${prefix}/var
docdir=${datarootdir}/doc
appdocdir=${docdir}/${APPNAME}
libdir=${exec_prefix}/lib
applibdir=${libdir}/${APPNAME}
mandir=${datarootdir}/man
man1dir=${mandir}/man1
mimedir=${datadir}/applications
srcdir=.
logdir=${localstatedir}/log
logfile=${logdir}/${APPNAME}.log

configfile=${sysconfdir}/${APPNAME}.conf

all:

install: installdirs
	$(shell awk 'NR==1 {print; \
		print "DATA_DIR='"${appdatadir}"'"; \
		print "LIB_DIR='"${applibdir}"'"; \
		print "LOG_FILE='"${logfile}"'"; \
		print "CONFIG_FILE='"${configfile}"'"} \
		NR!=1'  \
			${srcdir}/bin/${APPNAME} > ${DESTDIR}${bindir}/${APPNAME})
	chmod 755 ${DESTDIR}${bindir}/${APPNAME}

	${INSTALL_PROGRAM} ${srcdir}/bin/${APPNAME}-open ${DESTDIR}${bindir}
	@for file in $(shell cd ${srcdir}/${APPNAME}; find . -name '*.py'); do\
		${INSTALL_DATA} -D ${srcdir}/${APPNAME}/$$file ${DESTDIR}${applibdir}/$$file;\
	done
	${INSTALL_DATA} ${srcdir}/bin/shell-integration.sh bin/shell-integration.fish ${DESTDIR}${appdatadir}
	${INSTALL_DATA} ${srcdir}/${APPNAME}.desktop ${DESTDIR}${mimedir}
	touch ${DESTDIR}${logfile}
	chmod 666 ${DESTDIR}${logfile}
	${INSTALL_DATA} ${srcdir}/docs/${APPNAME}.1.gz ${DESTDIR}${man1dir}
	${INSTALL_DATA} ${srcdir}/docs/${APPNAME}.conf ${DESTDIR}${configfile}
	${INSTALL_DATA} ${srcdir}/docs/${APPNAME}.conf ${DESTDIR}${appdatadir}
	${INSTALL_DATA} ${srcdir}/README.md ${DESTDIR}${appdocdir}/README
	${INSTALL_DATA} ${srcdir}/copyright ${DESTDIR}${appdocdir}
	${INSTALL_DATA} ${srcdir}/changelog.md ${DESTDIR}${appdocdir}/changelog


installdirs:
	${INSTALL} -d ${DESTDIR}${bindir} ${DESTDIR}${applibdir} ${DESTDIR}${appdatadir} ${DESTDIR}${logdir}\
		${DESTDIR}${appdocdir} ${DESTDIR}${man1dir} ${DESTDIR}${mimedir} ${DESTDIR}${sysconfdir}

uninstall:
	@rm -rfv ${applibdir}
	@rm -rfv ${appdocdir} 
	@rm -rfv ${appdatadir} 
	@rm -rfv ${mimedir}/${APPNAME}.desktop
	@rm -rfv ${man1dir}/${APPNAME}.1.gz
	@rm -rfv ${logfile}
	@rm -rfv ${bindir}/${APPNAME}
	@rm -rfv ${bindir}/${APPNAME}-open
	@rm -rfv ${configfile}
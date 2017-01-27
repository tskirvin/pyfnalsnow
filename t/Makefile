RITM?= 'RITM456995'
GROUP?= 'SSI Internal'
USER?= 'tskirvin'

default: ritm

ritm:
	@echo "ritm"
	@ ../usr/bin/snow-ritm $(RITM)

ritm-debug:
	@echo "ritm-debug"
	@ ../usr/bin/snow-ritm $(RITM) --type debug

ritm-search:
	@echo "ritm-search"
	@ ../usr/bin/snow-ritm-list

include Makefile.incident

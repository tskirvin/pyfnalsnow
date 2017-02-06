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

ritm-assign:
	@echo "ritm-assign"
	@ ../usr/bin/snow-ritm-assign $(RITM) --user richt --group 'SSI Internal'

ritm-assign-no-user:
	@echo "ritm-assign-no-user"
	@ ../usr/bin/snow-ritm-assign $(RITM) --group 'SSI Internal' --debug

ritm-assign-no-group:
	@echo "ritm-assign-no-group"
	@ ../usr/bin/snow-ritm-assign $(RITM) --user richt --debug

ritm-audit:
	@echo "ritm-audit"
	@ ../usr/bin/snow-ritm $(RITM) --type audit


ritm-journal:
	@echo "ritm-journal"
	@echo "testing" | ../usr/bin/snow-ritm-journal $(RITM) 

ritm-search:
	@echo "ritm-search"
	@ ../usr/bin/snow-ritm-list


include Makefile.incident

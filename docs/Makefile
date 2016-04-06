UMLS=$(subst plantuml,png,$(wildcard *.plantuml))

all: $(UMLS)
	echo $(UMLS)

%.png: %.plantuml
	plantuml -tpng $<

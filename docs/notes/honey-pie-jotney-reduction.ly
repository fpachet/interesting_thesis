\version "2.24.3"
\pointAndClickOff
\paper {
  #(set-paper-size "a4")
  top-margin = 18\mm
  bottom-margin = 18\mm
  left-margin = 20\mm
  right-margin = 20\mm
  indent = 0
  ragged-last-bottom = ##t
  print-page-number = ##f
}
\header {
  title = "Honey Pie : le détour qui fait question"
  subtitle = "Cas Jotney - réduction analytique de travail"
  composer = "Chanson : John Lennon / Paul McCartney (1968)"
  tagline = ##f
}
\layout {
  \context { \Score \omit BarNumber }
  \context { \Staff \omit TimeSignature }
}
\markup \vspace #1
\markup \wordwrap {
  Schéma, non transcription de l'enregistrement. Les durées et les registres
  sont neutralisés ; les dispositions d'accords sont choisies pour la démonstration.
}
\markup \vspace #1
\markup \bold "1. Le point d'accroche : le motif de « crazy »"
\score {
  <<
    \new ChordNames \chordmode { ees1:7 s1 s1 }
    \new Staff {
      \clef treble \key g \major \cadenzaOn
      bes'1_\markup "si bémol" g'1_\markup "sol" bes'1_\markup "si bémol"
      \bar ""
    }
  >>
  \layout { ragged-right = ##t }
}
\markup \wordwrap {
  Le si bémol est étranger à la gamme de Sol majeur, mais appartient à Mi bémol 7 :
  il en est la quinte. Le repère est « crazy », non « lazy ».
  Hauteurs du motif d'après l'analyse de Matt Blick ; rythme original non reproduit.
}
\markup \vspace #1.5
\markup \bold "2. Du détour chromatique au retour tonal"
\score {
  <<
    \new ChordNames \chordmode { g1 ees1:7 e1:7 a1:7 d1:7 g1 }
    \new Staff {
      \clef treble \key g \major \cadenzaOn
      <g' b' d''>1 \bar "|"
      <ees' g' bes' des''>1 \bar "|"
      <e' gis' b' d''>1 \bar "|"
      <a cis' e' g'>1 \bar "|"
      <d' fis' a' c''>1 \bar "|"
      <g b d' g'>1 \bar "|."
    }
  >>
}
\markup \wordwrap {
  Les séparations distinguent les accords, pas les mesures du morceau.
  Mi bémol 7 - Mi 7 : approche chromatique ascendante, et non résolution
  dominante-tonique. Mi 7 - La 7 - Ré 7 - Sol : chaîne de dominantes.
}
\markup \vspace #1
\markup \wordwrap {
  Dans les deux positions centrales choisies, toutes les voix montent d'un demi-ton :
  mi bémol / mi ; sol / sol dièse ; si bémol / si ; ré bémol / ré.
  Cette réalisation illustre une possibilité de conduite des voix, pas le relevé
  de l'accompagnement original.
}
\markup \vspace #1.5
\markup \bold "3. De la surprise à la construction"
\markup \wordwrap {
  Question de travail : comment cette note trouve-t-elle sa place et comment
  ce détour rejoint-il Sol ? Comparer, reconstruire, puis réécouter : ces opérations
  donnent un contenu à « comment ça marche ? ». Leur simple possibilité ne prouve
  pas qu'elles se produisent chez chaque auditeur.
}
\markup \vspace #1.5
\markup \fontsize #-2 \column {
  \line { "Sources analytiques (consultées le 8 septembre 2026) :" }
  \line { "Matt Blick, « 10:21 Honey Pie (pt.2) », Beatles Songwriting Academy, 2 septembre 2013." }
  \line { "beatlessongwriting.blogspot.com/2013/09/1021-honey-pie-pt2.html" }
  \line { "Alan W. Pollack, Notes on « Honey Pie », 21 juin 1998 :" }
  \line { "www.icce.rug.nl/~soundscapes/DATABASES/AWP/hp.shtml" }
  \line { "Dossier et limites : docs/notes/honey-pie-jotney.md" }
}

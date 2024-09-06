---
title: 'Hydrogen-Transport-Materials: An Open-Source Database for Hydrogen Transport Properties'
tags:
  - Python
  - hydrogen transport
  - database
  - visualisation
authors:
  - name: Remi Delaporte-Mathurin
    corresponding: true
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: James Dark
    affiliation: "2, 3"
  - name: Thomas Fuerst
    affiliation: 4

affiliations:
 - name: Plasma Science and Fusion Center, MIT, USA
   index: 1
   ror: 00hx57361
 - name: IRFM, CEA, France
   index: 2
 - name: LSPM, CNRS, France
   index: 3
 - name: Idaho National Lab, USA
   index:
 
date: 6 September 2024
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

The forces on stars, galaxies, and dark matter under external gravitational
fields lead to the dynamical evolution of structures in the universe. The orbits
of these bodies are therefore key to understanding the formation, history, and
future state of galaxies. The field of "galactic dynamics," which aims to model
the gravitating components of galaxies to study their structure and evolution,
is now well-established, commonly taught, and frequently used in astronomy.
Aside from toy problems and demonstrations, the majority of problems require
efficient numerical tools, many of which require the same base code (e.g., for
performing numerical orbit integration).

# Statement of need

Hydrogen transport properties are critical for a wide range of applications, from energy storage and fuel cells [@H-Storage_Schlapbach_2001][@H-Storage_Ren_2017], hydrogen embrittlement studies in materials science 
[@Embrittlement_Oriani_1978][@Embrittlement_Li_2020], to safety studies in nuclear applications [@forsberg2017tritium][@osti_1777267][@abdou2020physics].
Researchers in these fields are highly dependent on accurate and comprehensive data on properties such as diffusivity, solubility, and recombination and dissociation coefficients.
Traditionally, these data have been scattered across numerous research papers, creating significant challenges for those who need to aggregate, standardise and interpret the information.

To address this issue, some researchers have undertaken the task of compiling review papers that aggregate data from various sources [REFs].
However, these traditional literature reviews suffer from several critical drawbacks.
Firstly, the manual aggregation process is prone to errors, including copy-paste mistakes, typos, and unit conversion errors.
Additionally, inconsistencies in data fitting and referencing often arise, further complicating the reliability of these reviews.

Another major issue is the lack of transparency in traditional reviews.
The methodologies and sources used are not always clear, making it difficult for other researchers to verify the accuracy of the compiled data. For example, whether a property is given in units of H atoms or H2 molecules, various unit conversions with undefined parameters such as temperature or density, or as simple as a paper not including the units of the properties.  
Moreover, once published, these reviews become static documents that do not accommodate new data or corrections, leading to obsolescence.
As new research emerges, the reviews quickly become outdated, and errors that are identified post-publication are rarely, if ever, corrected.

Given these challenges, there is a pressing need for a more reliable, accessible, and up-to-date approach to aggregating hydrogen transport properties.
This paper proposes the Hydrogen Transport Materials (HTM) database as a modern solution to these problems.
HTM is an online, open-source database designed to provide accurate, transparent, and continuously updated data on hydrogen transport properties.

Unlike traditional literature reviews, HTM offers several key advantages.
It automates unit conversion and data fitting processes, significantly reducing the potential for human error.
The database is also designed to be transparent, with all sources and methodologies clearly documented.
Furthermore, HTM is a living database that can be continuously updated with new data, ensuring that researchers always have access to the most current information.
The open-source nature of HTM allows for community contributions and corrections, fostering a collaborative and dynamic research environment.

In this paper, we will discuss the key hydrogen transport properties, describe the features and architecture of the HTM database, outline the workflow for contributing to and maintaining the database, and compare HTM with traditional literature reviews.
We will also explore the future directions for HTM, including potential improvements and applications.

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from [insert HTM contributions]

# References

# Optimal Inversion Time Extractor on Cardiac MRIs
________

### Project Context

MRIs images are largely used for the evaluation of myocardiac scar and other cardiac anomalies diagnosis.
Bordeaux's Institute of Cardiology (IHU-Liryc) recently developped a technique based on black-blood capable of 
augmenting the contrast between blood signals and muscular tissues on MRIs. They inject a contrast agent called 
Galothinium to get this better visualization
The black Blood MRI images they generate contain a sequence of MRI generated at different
instants. Image contrast vary with time as it impregnates gradually the muscle tissues.

''' Insert the graphic image with optimal time inversion '''

The contrast is the best on MRIs images when blood signal is null.
However, the selection of the optimal inversion time TI (instant 
for which MRI has the best rendering) is quite challenging. The chosen image must be always exploitable 
in order to favor cardiac diagnosis. Otherwise, we could miss important pathologies.

This project is aimed to propose an algorithm based on CNN to extract automatically the image corresponding
to the optimal TI. It would enable radiologs to gain much time in their work, by studying directly on treated images.

## Project Structure

### Several remarks
1. Ground Truth annotations done by several people, to have a consensus on best image renderings
   (generate an app capable to automatize this annotation)

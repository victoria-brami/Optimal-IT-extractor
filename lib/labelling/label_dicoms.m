%This function will create a loop on the patients MRIs and propose
% to the user to label the images (if they corresponds to optimal IT or
% not)

% add path to imagine viewer
addpath(genpath('/Users/victoria.brami/Documents/'))
ROOT = '/Users/victoria.brami/Documents/';

%patient_ids = {'37', '39', '40', '44', '45', '50', '52', '55','59', '60','62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '75', '76', '77', '81', '82', '84', '86', '92', '99', '100', '101', '106', '108', '109', '110', '111', '112', '114', '115', '116', '120', '122', '123', '124', '125', '128'};
patient_ids = {'37', '39'};
optimal_indexes = zeros(length(patient_ids), 12);
user_indexes_val = 0;
opt = 0;
patient_index = 1;

for patient_name = patient_ids
    % Load and diplay sequences
    namefile = fullfile(ROOT, 'Optimal-IT-Extractor', 'data', 'TIScoutBlackBlood', patient_name{1}, 'data.mat');
    load(namefile);
    imagine_bis(img);
    
    % message box for data annotations
    prompt = {'Enter space-separated optimal indexes (varying from 1 to 11):'};
    dlgtitle = 'OPTIMAL TI ANNOTATION';
    dims = [1, 60];
    mri_optimal_indexes = inputdlg(prompt, dlgtitle, dims);
    
    % Append the new indexes (convert them to numerals)
    
    %first column in the patient id
    optimal_indexes(patient_index, 1) = str2num(patient_name{1});
    opt = str2num(mri_optimal_indexes{1});
    for ti_index = opt
        optimal_indexes(patient_index, ti_index + 1) = 1;
    end
    patient_index = patient_index + 1;
    
end  

% Store the results in csv file
fprintf( '%d ', user_indexes_val ); fprintf('\n')
writematrix(optimal_indexes, 'TI_labels.csv');
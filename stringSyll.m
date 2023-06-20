function data = stringSyll(file)
%Use python syllabification algorithms to syllabify all words in a
%sentence. Takes information on word- and phone-level transcription
%(word/phone identity and times) from mat file (struct) and creates a
%struct where each syllable is a row with columns:
%   LABEL = identity of syllable (string of phones)
%   OFFS = vector with start (1st position) and end (2nd position) of syll
%   POS = Position of syllable in word (S1 = 1st, S2 = 2nd, etc.)
%   TYPE = # of onset and coda consonants (e.g., "O2C0" = CCV syllable)
%   STRESS = lexical stress (1 = primary, 2 = secondary, 0 = unstressed)
%   PARTS = embedded struct with list of onset, nucleus, and coda phones
%   TIMES = N x 2 matrix with start/end times of each subsyllabic unit
%       N = number of subsyllabic units (max. 3 for syllable with both
%       onset and coda)
%       1st column = start times, 2nd column = end times
%Input FILE is a saved struct in Mark Tiede's standard format (e.g., separate
%WORD and PHONE fields with LABEL and OFFS)

data = LoadMAT(file);

sylled = [];
wrdlst = [];
syllStruct = struct('LABEL', {}, 'OFFS', {}, 'POS',{}, 'TYPE', {}, 'STRESS', {}, ...
    'PARTS', {}, 'TIMES', {});
si = 1;
for wi = 1:size(data(1).WORDS,2)
    snew = sylled;
    phoneList = "";
    phoneListCol = [];
    phoneStarts = [];
    phoneEnds = [];
    wrd = data(1).WORDS(wi).LABEL; %WORDS.LABEL = word identity (orthography)
    wrdStrt = data(1).WORDS(wi).OFFS(1); %WORDS.OFFS(1) = word start time
    wrdEnd = data(1).WORDS(wi).OFFS(2); %WORDS.OFFS(2) = word end time
    pi = 1;
    if wrd == "sp"
        continue;
    end
    
    %loop to determine which phones are within a word
    %(don't remember why I used an if loop within the while loop 
    %instead of combining the start and end conditions in the while condition)
    while data(1).PHONES(pi).OFFS(2) <= wrdEnd %PHONES.OFFS(2) = phone end times
        if data(1).PHONES(pi).OFFS(1) >= wrdStrt %PHONES.OFFS(1) = phone start times
            phoneList = append(phoneList, " ", data(1).PHONES(pi).LABEL);
            phoneStarts = [phoneStarts; data(1).PHONES(pi).OFFS(1)];
            phoneEnds = [phoneEnds; data(1).PHONES(pi).OFFS(2)];
        end
        pi = pi + 1; 
    end
    phoneTimes = [phoneStarts, phoneEnds];
    if length(phoneStarts) == 1
        phoneTimes = [phoneTimes; [0,0]];
    end

    %make sure python's not going to throw a temper tantrum
    if count(py.sys.path, '') == 0
        insert(py.sys.path, int32(0), '');
    end
    if count(py.sys.path,'Users/sarahharper/Dropbox/ChangLab/Syllable_Boundary/Code') == 0
        insert(py.sys.path,int32(0),'Users/sarahharper/Dropbox/ChangLab/Syllable_Boundary/Code');
    end
    
    %run syllabification algorithm in python
 %    syllsyll = py.word_syllabification.syllWord(phoneList, py.numpy.array(phoneTimes), "basic");
     syllsyll = pyrunfile(...
           '/Users/sarahharper/Dropbox/ChangLab/Syllable_Boundary/Code/syllabification_wrapper.py',...
           "outsyll", phonemes = phoneList, phoneTimes = py.numpy.array(phoneTimes), alg = "basic");
     sylled{wi,1} = syllsyll;
    
    %build matlab-friendly output struct from output python dict
    syllsyll = struct(syllsyll);
    sf = fieldnames(syllsyll);
    for ss = 1: length(sf)
        syllStruct(si).LABEL = sf{ss,1}; %get ident of current syllable & add to struct
        syllStats = struct(syllsyll.(sf{ss,1})); %get embedded dict with the actual derived info about syllable at this index
        syllStruct(si).TYPE = string(syllStats.stype);
        syllStruct(si).POS = string(syllStats.snum);
        syllStruct(si).STRESS = string(syllStats.sstress);
        syllStruct(si).PARTS = struct(syllStats.parts);
        syllStruct(si).PARTS(1).ons = string(syllStruct(si).PARTS(1).ons);
        syllStruct(si).PARTS(1).nuc = string(syllStruct(si).PARTS(1).nuc);
        syllStruct(si).PARTS(1).coda = string(syllStruct(si).PARTS(1).coda);
        %create array with start and end times of all syllable
        %subcomponents & add to struct
        if startsWith(string(syllStats.stype), "O0") & endsWith(string(syllStats.stype), "C0")
            syllStruct(si).TIMES = [cellfun(@double, cell(syllStats.nucTimes))];
        elseif startsWith(string(syllStats.stype), "O0")
            syllStruct(si).TIMES = [cellfun(@double, cell(syllStats.nucTimes)); ...
                cellfun(@double, cell(syllStats.codaTimes))];
        elseif endsWith(string(syllStats.stype), "C0")
            syllStruct(si).TIMES = [cellfun(@double, cell(syllStats.onsTimes)); ...
                cellfun(@double, cell(syllStats.nucTimes))];
        else
            syllStruct(si).TIMES = [cellfun(@double, cell(syllStats.onsTimes)); ...
                cellfun(@double, cell(syllStats.nucTimes)); cellfun(@double, cell(syllStats.codaTimes))];
        end
        
        %get OFFS [start & end times] for current syllable & add to struct
        if startsWith(string(syllStats.stype), "O0") %get start time of syllable - depends on whether or not onset
            syllStart = cell(syllStats.nucTimes(1));
        else
            syllStart = cell(syllStats.onsTimes(1));
        end
        syllStart = cellfun(@double, syllStart);
        if endsWith(string(syllStats.stype), "C0") %get end time of syllable - depends on whether or not coda
            syllEnd = cell(syllStats.nucTimes(2));
        else
            syllEnd = cell(syllStats.codaTimes(2));
        end
        syllEnd = cellfun(@double, syllEnd);
        syllOffs = [syllStart, syllEnd];
        syllStruct(si).OFFS = syllOffs; %add syll times to struct
        si = si + 1;
    end
data(1).SYLL = syllStruct;
fname = [file '_SYLL'];
SaveVar(data, fname)
end


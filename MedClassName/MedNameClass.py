
class MedicationChecker:
    
    # PPI = Proton Pump Inhibitor
    ppi_generic = ['dexlansoprazole','esomeprazole','lansoprazole','omeprazole','pantoprazole','rabeprazole']
    ppi_brand = ['dexilant','nexium','prevacid','prilosec','protonix','aciphex','kapidex','konvomep','vimovo','zegerid']

    # AHG = Anti-Hyperglycemic
    ahg_brand = [
    'acarbose', 'acetohexamide', 'actoplus', 'actos', 'adlyxin', 'admelog', 'afrezza', 'alogliptin', 
    'alogliptin-metformin', 'alogliptin-pioglitazone', 'amaryl', 'apidra', 'appformin', 'appformin-d', 
    'avandamet', 'avandaryl', 'avandia', 'basaglar', 'bexagliflozin', 'brenzavvy', 'bydureon', 'byetta', 
    'chlorabetic', 'chlorpropamide', 'cycloset', 'dapagliflozin', 'dapagliflozin-metformin', 'diabeta', 
    'diabinese', 'dibatrol', 'dm2', 'duetact', 'dymelor', 'exubera', 'farxiga', 'fiasp', 'fortamet', 
    'glimepiride', 'glipizide', 'glipizide-metformin', 'glucamide', 'glucophage', 'glucotrol', 'glucovance', 
    'glumetza', 'glyburide', 'glyburide-metformin', 'glycron', 'glynase', 'glyset', 'glyxambi', 'humalog', 
    'humulin', 'icn-tolam', 'iletin', 'increlex', 'inpefa', 'insulase', 'insulatard', 'insulin', 'invokamet', 
    'invokana', 'iplex', 'isophane', 'janumet', 'januvia', 'jardiance', 'jentadueto', 'juvisync', 'kazano', 
    'kombiglyze', 'korlym', 'lantus', 'lentard', 'lente', 'levemir', 'lyumjev', 'metaglip', 'metformin', 
    'micronase', 'mifepristone', 'miglitol', 'mixtard', 'monotard', 'mounjaro', 'myxredlin', 'nateglinide', 
    'nesina', 'novolin', 'novolog', 'onglyza', 'oribetic', 'orinase', 'oseni', 'ozempic', 'pioglitazone', 
    'pioglitazone-glimepiride', 'pioglitazone-metformin', 'prandimet', 'prandin', 'precose', 'protamine', 
    'purified', 'qtern', 'relion', 'repaglinide', 'repaglinide-metformin', 'rezulin', 'rezvoglar', 'riomet', 
    'ronase', 'rybelsus', 'saxagliptin', 'saxagliptin-metformin', 'segluromet', 'semglee', 'sk-tolbutamide', 
    'soliqua', 'starlix', 'steglatro', 'steglujan', 'symlin', 'symlinpen', 'synjardy', 'tanzeum', 'tolamide', 
    'tolazamide', 'tolbutamide', 'tolinase', 'toujeo', 'tradjenta', 'tresiba', 'trijardy', 'trulicity', 
    'velosulin', 'victoza', 'xigduo', 'xultophy', 'zituvio']

    ahg_generic = [
    'acarbose', 'acetohexamide', 'albiglutide', 'alogliptin', 'bexagliflozin', 'bromocriptine', 'canagliflozin', 
    'canagliflozin/metformin', 'chlorpropamide', 'dapaglifloz', 'dapagliflozin', 'dapagliflozin/saxagliptin', 
    'dulaglutide', 'empaglifloz/linaglip/metformin', 'empagliflozin', 'empagliflozin/linagliptin', 
    'empagliflozin/metformin', 'ertugliflozin', 'ertugliflozin/metformin', 'ertugliflozin/sitagliptin', 
    'exenatide', 'glimepiride', 'glipizide', 'glipizide/metformin', 'glyburide', 'glyburide,micronized', 
    'glyburide/metformin', 'ins', 'insul,pk', 'insulin', 'insulin,beef', 'insulin,pork', 'linagliptin', 
    'linagliptin/metformin', 'liraglutide', 'lixisenatide', 'mecasermin', 'metformin', 'metformin/aa', 
    'metformin/blood', 'metformin/caff/aa7/hrb125/chol', 'mifepristone', 'miglitol', 'nateglinide', 
    'pioglitazone', 'pramlintide', 'reg', 'repaglinide', 'repaglinide/metformin', 'rosiglitazone', 
    'rosiglitazone/glimepiride', 'rosiglitazone/metformin', 'saxagliptin', 'semaglutide', 'sitagliptin', 
    'sotagliflozin', 'tirzepatide', 'tolazamide', 'tolbutamide', 'troglitazone']

    # AP = Antipsychotic
    ap_brand = [
    'abilify', 'adasuve', 'aripiprazole', 'aristada', 'asenapine', 'caplyta', 'chloramead', 'chlorpromazine', 
    'clorazine', 'clozapine', 'clozaril', 'droperidol', 'fanapt', 'fazaclo', 'fluphenazine', 'foypromazine', 
    'geodon', 'haldol', 'haloperidol', 'halperon', 'inapsine', 'invega', 'kenazine', 'klorazine', 'latuda', 
    'loxapine', 'loxitane', 'lurasidone', 'lybalvi', 'melacen', 'mellaril', 'mellaril-s', 'millazine', 'moban', 
    'molindone', 'myperidol', 'navane', 'olanzapine', 'ormazine', 'paliperidone', 'permitil', 'perphenazine', 
    'perseris', 'prolixin', 'quetiapine', 'rexulti', 'risperdal', 'risperidone', 'rykindo', 'saphris', 'secuado', 
    'serentil', 'seroquel', 'sk-thioridazine', 'sparine', 'stelaprin', 'stelazine', 'thioridazine', 'thiothixene', 
    'thoradol', 'thoramed', 'thorarex', 'thorazine', 'trifluoperazine', 'trilafon', 'uzedy', 'versacloz', 
    'vesprin', 'vraylar', 'ziprasidone', 'zyprexa']

    ap_generic = [
    'aripiprazole', 'asenapine', 'brexpiprazole', 'cariprazine', 'chlorpromazine', 'clozapine', 'droperidol', 
    'fluphenazine', 'haloperidol', 'iloperidone', 'loxapine', 'lumateperone', 'lurasidone', 'mesoridazine', 
    'molindone', 'olanzapine', 'olanzapine/samidorphan', 'paliperidone', 'perphenazine', 'promazine', 
    'quetiapine', 'risperidone', 'thioridazine', 'thiothixene', 'trifluoperazine', 'triflupromazine', 
    'ziprasidone']

    # BENZO = Benzodiazepine
    benzo_brand = [
    'alprazolam', 'a-poxide', 'ativan', 'calmium', 'cdp', 'chlor', 'chlordiazepoxide', 'clorazepate', 
    'colspan', 'dalmane', 'diazepam', 'di-tran', 'dizac', 'doral', 'dormalin', 'd-tran', 'd-val', 'estazolam', 
    'flurazepam', 'gen-xene', 'halcion', 'h-tran', 'icn-azepox', 'j-tran', 'kenrax', 'libaca', 'libritabs', 
    'librium', 'lipoxide', 'lorazepam', 'lorazepam-0.9%', 'lorazepam-d5w', 'lorazepam-ns', 'loreev', 'midazolam', 
    'mitran', 'm-tran', 'murcil', 'niravam', 'oxazepam', 'paxipam', 'poxi', 'prosom', 'q-pam', 'quazepam', 
    'restoril', 'ro-azepam', 'ro-poxide', 'serax', 'sereen', 'sk-lygen', 'spaz-10', 'spaz-5', 'temazepam', 
    'tranxene', 'tranxene-t', 'triazolam', 'valium', 'versed', 'xanax', 'zetran']

    benzo_generic = [
    'alprazolam', 'chlordiazepoxide', 'clorazepate', 'diazepam', 'estazolam', 'flurazepam', 'halazepam', 
    'lorazepam', 'midazolam', 'oxazepam', 'quazepam', 'temazepam', 'triazolam']

    # CI = Cholinesterase Inhibitor or memantine
    ci_brand = [
    'adlarity', 'anticholium', 'antidote', 'antilirium', 'aricept', 'bloxiverz', 'cognex', 'donepezil', 
    'duodote', 'edrophonium', 'enlon', 'enlon-plus', 'exelon', 'galantamine', 'mestinon', 'mytelase', 
    'neostigimine', 'neostigmine', 'neostigmine-sterile', 'physostigmine', 'pralidoxime', 'prostigmin', 
    'protopam', 'pyridostigmine', 'razadyne', 'regonol', 'reminyl', 'reversol', 'rivastigmine', 'tensilon', 'namenda'
    ]

    ci_generic = [
    'ambenonium', 'donepezil', 'edrophonium', 'galantamine', 'neostigmine', 'physostigmine', 'pralidoxime', 
    'pyridostigmine', 'rivastigmine', 'tacrine','memantine'
    ]
    
    #start the functions to check if the input string contains a medication
    def contains_ppi(self, input_string):
        input_string = input_string.lower()
        for ppi in self.ppi_generic:
            if ppi in input_string:
                return 'PPI'
        for ppi in self.ppi_brand:
            if ppi in input_string:
                return 'PPI'
        return 'NA'

    def contains_ahg(self,input_string):
        input_string = input_string.lower()
        for ahg in self.ahg_brand:
            if ahg in input_string:
                return 'AHG'
        for ahg in self.ahg_generic:
            if ahg in input_string:
                return 'AHG'
        return 'NA'

    def contains_ap(self,input_string):
        input_string = input_string.lower()
        for ap in self.ap_brand:
            if ap in input_string:
                return 'AP'
        for ap in self.ap_generic:
            if ap in input_string:
                return 'AP'
        return 'NA'
    
    def contains_benzo(self,input_string):
        input_string = input_string.lower()
        for benzo in self.benzo_brand:
            if benzo in input_string:
                return 'BENZO'
        for benzo in self.benzo_generic:
            if benzo in input_string:
                return 'BENZO'
        return 'NA'

    def contains_ci(self,input_string):
        input_string = input_string.lower()
        for ci in self.ci_brand:
            if ci in input_string:
                return 'CI'
        for ci in self.ci_generic:
            if ci in input_string:
                return 'CI'
        return 'NA'
    
#use the class to check if the input string contains a medication
checker = MedicationChecker()

#examples for checking 
ppi_ex = 'Omeprazole 20mg Capsule'
ahg_ex = 'Metformin 500mg Tablet'
ap_ex = 'Quetiapine 100mg Tablet'
benzo_ex = 'Alprazolam 1mg Tablet'
ci_ex = 'Donepezil 5mg Tablet'

na_ex = 'Linezolid 600mg Tablet'

print(checker.contains_ppi(ppi_ex))
print(checker.contains_ahg(ahg_ex))
print(checker.contains_ap(ap_ex))
print(checker.contains_benzo(benzo_ex))
print(checker.contains_ci(ci_ex))

print(checker.contains_ppi(na_ex))
print(checker.contains_ahg(na_ex))
print(checker.contains_ap(na_ex))
print(checker.contains_benzo(na_ex))
print(checker.contains_ci(na_ex))
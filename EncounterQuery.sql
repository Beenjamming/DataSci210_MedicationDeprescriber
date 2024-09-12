use CDW_NEW;

IF OBJECT_ID('tempdb.dbo.#encs', 'U') IS NOT NULL  DROP TABLE #encs;
SELECT			ef.EncounterKey
				,ef.PatientKey
				,pat.Sex
				,isnull(age.Years,datediff(year,pat.birthdate,admitdt.datevalue)) "Age_y"
				,pat.BirthDate
				,admitdt.DateValue "PtAdmitDate"
				,disdt.DateValue "PtDischargeDate"
				,drg.Name "DRG"
				,ef.FinancialClass
				,ef.AdmissionOrigin
				,ef.AdmissionSource
				,ef.AdmissionType
				,pdiag.Name "PrimaryDx"
				,ef.PresentOnAdmissionDiagnosisComboKey
				,ef.HospitalAcquiredDiagnosisComboKey
				,ef.DischargeDisposition
				,ef.DischargePatientClass
				
into #encs
  FROM [CDW_NEW].[deid].HospitalAdmissionFact ef 
  left join patientdim pat on ef.PatientKey = pat.PatientKey
  left join DateDim admitdt on ef.InpatientAdmissionDateKey = admitdt.DateKey 
  left join DateDim disdt on ef.DischargeDateKey = disdt.DateKey 
  left join DurationDim age on ef.AgeKey = age.DurationKey
  left join DrgDim drg on ef.DrgKey = drg.DrgKey
  left join DiagnosisDim pdiag on ef.PrimaryCodedDiagnosisKey = pdiag.DiagnosisKey
  where disdt.DateValue between '09/01/2023' and '09/30/2023' and ef.DischargePatientClass = 'Inpatient' 
  

IF OBJECT_ID('tempdb.dbo.#orders', 'U') IS NOT NULL  DROP TABLE #orders;
select mof.EncounterKey
		,mof.PatientKey
		,mof.MedicationOrderKey 
		,orderdt.DateValue "OrderDate"
		,mof.OrderName
		,mof.Frequency
		,mof.Sig
		,mof.Quantity
		,mof.QuantityUnit
		,dur.Days "DurationDays"
		,mof.Mode
		,mof.Class
		,mof.[Source]
		,case when mof.Source like '%Discharge%' then 1 else 0 end "DischargeOrder"
		,erx.Name
		,erx.PharmaceuticalClass
		,erx.PharmaceuticalSubclass
		,erx.TherapeuticClass
		,mof.AssociatedDiagnosisComboKey
		
into #orders 
from CDW_NEW.deid.MedicationOrderFact mof 
join datedim orderdt on mof.OrderedDateKey = orderdt.DateKey
join MedicationDim erx on mof.MedicationKey = erx.MedicationKey
left join durationdim dur on mof.DurationKey = dur.DurationKey
where mof.EncounterKey in (select e.EncounterKey from #encs e)
and erx.PharmaceuticalClass like '%proton%'


IF OBJECT_ID('tempdb.dbo.#dx', 'U') IS NOT NULL  DROP TABLE #dx;
select o.MedicationOrderKey
		,dd.Name "Diagnosis"
into #dx 
from #orders o
left join DiagnosisBridge db on o.AssociatedDiagnosisComboKey = db.DiagnosisComboKey
join DiagnosisDim dd on db.DiagnosisKey = dd.DiagnosisKey

--encounters
select * 
from #encs 
where #encs.EncounterKey in (select EncounterKey from #orders where #orders.Mode = 'Outpatient' and #orders.DischargeOrder = 1)

--orders
select	o.*
		,stuff((select distinct ', ' + dx.Diagnosis from #dx dx										
						where o.MedicationOrderKey = dx.MedicationOrderKey 
						FOR XML PATH('')), 1, 2, '') "OrderDx"
from #orders o 
where o.EncounterKey in (select EncounterKey 
						from #encs 
						where #encs.EncounterKey in (select EncounterKey from #orders where #orders.Mode = 'Outpatient' and #orders.DischargeOrder = 1))


--hosp acquired dx 
select e.EncounterKey
		,dd.*  

from #encs e 
left join DiagnosisBridge db on e.HospitalAcquiredDiagnosisComboKey = db.DiagnosisComboKey
left join DiagnosisDim dd on db.DiagnosisKey = dd.DiagnosisKey
order by 1 

--present on admit dx
select e.EncounterKey
		,dd.*  

from #encs e 
left join DiagnosisBridge db on e.PresentOnAdmissionDiagnosisComboKey = db.DiagnosisComboKey
left join DiagnosisDim dd on db.DiagnosisKey = dd.DiagnosisKey
order by 1 

--note_text
select nm.deid_note_key,nm.EncounterKey, replace(nt.note_text,'|','') "NoteText"
from (select nm.* 
from CDW_Notes.notes.note_metadata nm
where nm.EncounterKey in (select #encs.EncounterKey from #encs)) nm
join CDW_Notes.notes.note_text nt on nm.deid_note_key = nt.deid_note_key
order by 1 

--note_concepts
select nm.deid_note_key,nm.EncounterKey, nc.domain, nc.confidence, nc.canon_text
from (select nm.* 
from CDW_Notes.notes.note_metadata nm
where nm.EncounterKey in (select #encs.EncounterKey from #encs)) nm
join CDW_Notes.notes.note_concepts nc on nm.deid_note_key = nc.deid_note_key
order by 1 

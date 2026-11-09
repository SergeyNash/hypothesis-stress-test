import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import validate_runs as validator
from service_profile import validate_service_outputs


class Contracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name)/'HYP-2026-11-09-001'
        shutil.copytree(ROOT/'examples/example-005', self.run)

    def tearDown(self):
        self.temp.cleanup()

    def edit(self, name, old, new):
        p = self.run/name
        text = p.read_text()
        self.assertIn(old, text)
        p.write_text(text.replace(old, new))

    def test_existing_product_examples_and_service_example(self):
        for run in sorted((ROOT/'examples').glob('example-00*')):
            with self.subTest(run=run.name):
                self.assertEqual([], validator.validate_complete_run(run))

    def test_service_requires_profile_specific_fields(self):
        self.edit('input/hypothesis.md', '- Текущий способ: мониторинг и ручной разбор; инженер клиента согласует изменения', '')
        self.assertIn('MISSING_SERVICE_FIELD', validator.validate_input(self.run, check_folder_id=True))

    def test_unknown_profile_rejected(self):
        self.edit('input/hypothesis.md', 'Профиль применения: service_business', 'Профиль применения: custom')
        self.assertIn('INVALID_PROFILE', validator.validate_input(self.run, check_folder_id=True))

    def test_unknown_hypothesis_type_rejected(self):
        self.edit('input/hypothesis.md', 'Тип гипотезы: delivery_model', 'Тип гипотезы: unspecified')
        self.assertIn('INVALID_HYPOTHESIS_TYPE', validator.validate_input(self.run, check_folder_id=True))

    def test_explicit_unknown_service_conditions_are_valid(self):
        self.edit('input/hypothesis.md', 'Изменение у поставщика: новая проактивная модель и коммерческая надстройка, включая сопровождение агента и знаний', 'Изменение у поставщика: неизвестно')
        self.assertEqual([], validator.validate_input(self.run, check_folder_id=True))

    def test_missing_metadata_fails(self):
        p = self.run/'input/hypothesis.md'
        p.write_text('\n'.join(line for line in p.read_text().splitlines()
                               if not any(label in line for label in ['Дата создания:', 'ID прогона:', 'Статус:'])))
        self.assertIn('MISSING_SECTION', validator.validate_input(self.run, check_folder_id=True))

    def test_localized_status_requires_repair(self):
        self.edit('input/hypothesis.md', 'Статус: completed', 'Статус: завершено')
        self.assertIn('INVALID_STATUS', validator.validate_input(self.run, check_folder_id=True))

    def test_no_if_syntax_requirement(self):
        self.edit('input/hypothesis.md', 'Если предложить', 'Предложение позволит предложить')
        self.assertEqual([], validator.validate_input(self.run, check_folder_id=True))

    def test_empty_context_field_rejected(self):
        self.edit('input/hypothesis.md', 'Домен: развитие поддержки корпоративного системного ПО', 'Домен:')
        self.assertIn('MISSING_CONTEXT_FIELD', validator.validate_input(self.run, check_folder_id=True))

    def test_missing_output_does_not_hide_behind_marker(self):
        (self.run/'outputs/customer_discovery_plan.md').unlink()
        codes = validator.validate_complete_run(self.run)
        self.assertIn('MISSING_MARKER_ARTIFACT', codes)

    def test_marker_inputs_must_match_registry(self):
        p = self.run/'outputs/customer_discovery_planning_complete.marker'
        value = json.loads(p.read_text()); value['inputs'] = []; p.write_text(json.dumps(value))
        self.assertIn('INVALID_MARKER_INPUTS', validator.validate_complete_run(self.run))

    def test_malformed_marker_does_not_crash(self):
        (self.run/'outputs/business_context_complete.marker').write_text('finished')
        self.assertIn('NON_CANONICAL_MARKER', validator.validate_complete_run(self.run))

    def test_missing_service_status_fails(self):
        self.edit('outputs/decision_review.md', '- provider_economics: conditional', '')
        self.assertIn('INVALID_SERVICE_STATUS', validate_service_outputs(self.run))

    def test_unknown_service_decision_fails(self):
        self.edit('outputs/decision_review.md', '- service_decision: limited_pilot', '- service_decision: build_everything')
        self.assertIn('INVALID_SERVICE_DECISION', validate_service_outputs(self.run))

    def test_synthetic_cannot_authorize_sales_expansion(self):
        self.edit('outputs/decision_review.md', 'limited_pilot', 'expand_sales')
        self.edit('outputs/decision_review.md', 'proceed_with_validation', 'proceed')
        self.edit('outputs/decision_review.md', 'Уверенность: Низкая', 'Уверенность: Высокая')
        for field in ['customer_value', 'delivery_feasibility', 'provider_economics']:
            self.edit('outputs/decision_review.md', f'- {field}: conditional', f'- {field}: supported')
        self.edit('outputs/decision_review.md', '- buying_path: unknown', '- buying_path: supported')
        self.assertIn('UNSUPPORTED_SALES_EXPANSION', validate_service_outputs(self.run))

    def test_real_supported_expansion_structurally_valid(self):
        # Syntax only: the validator cannot establish that alleged evidence is true.
        self.edit('outputs/evidence_inventory.md', 'source_origin: synthetic', 'source_origin: provider_record')
        self.edit('outputs/evidence_inventory.md', 'evidence_status: synthetic', 'evidence_status: observed')
        self.edit('outputs/decision_review.md', 'limited_pilot', 'expand_sales')
        self.edit('outputs/decision_review.md', 'proceed_with_validation', 'proceed')
        self.edit('outputs/decision_review.md', 'Уверенность: Низкая', 'Уверенность: Высокая')
        self.edit('outputs/human_report.html', 'data-service-decision="limited_pilot"', 'data-service-decision="expand_sales"')
        for field, old in [('customer_value','conditional'),('buying_path','unknown'),('delivery_feasibility','conditional'),('provider_economics','conditional')]:
            self.edit('outputs/decision_review.md', f'- {field}: {old}', f'- {field}: supported')
            self.edit('outputs/human_report.html', f'data-service-field="{field}" data-status="{old}"', f'data-service-field="{field}" data-status="supported"')
        self.assertEqual([], validate_service_outputs(self.run))

    def test_html_cannot_upgrade_status(self):
        self.edit('outputs/human_report.html', 'data-status="unknown"', 'data-status="supported"')
        self.assertIn('SERVICE_REPORT_MISMATCH', validate_service_outputs(self.run))

    def test_validation_plan_requires_stopping_and_branches(self):
        self.edit('outputs/customer_discovery_plan.md', 'Критерий остановки', 'Другое')
        self.assertIn('INCOMPLETE_SERVICE_VALIDATION_PLAN', validate_service_outputs(self.run))

    def test_provenance_required(self):
        self.edit('outputs/evidence_inventory.md', '- source_origin: synthetic', '')
        self.assertIn('MISSING_SERVICE_PROVENANCE', validate_service_outputs(self.run))

    def test_pending_source_review_cannot_be_a_completed_run(self):
        p = self.run/'outputs/evidence_inventory.md'
        p.write_text(p.read_text() + '\n## Проверка полноты\n- status: pending\n')
        self.assertIn('INCOMPLETE_RETRIEVAL_REVIEW', validator.validate_complete_run(self.run))
        p.write_text(p.read_text().replace('status: pending', 'status: accepted'))
        self.assertEqual([], validator.validate_complete_run(self.run))

    def test_contract_arithmetic(self):
        self.assertEqual(15000, 90000 - 18*3000 - 12000 - 9000)
        self.assertEqual(-21000, 90000 - 30*3000 - 12000 - 9000)
        self.assertEqual(-57000, 15000 - 24*3000)
        self.assertEqual(23, (90000-12000-9000)/3000)
        self.assertGreater(2*(24+18), 640-440-120)


if __name__ == '__main__':
    unittest.main()

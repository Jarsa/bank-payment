# © 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestBank(BaseCommon):
    # Keep running the tests as the environment user, like account's own tests
    _test_user_groups = None

    def test_bank(self):
        bank = self.env["res.partner.bank"].create(
            {
                "account_number": "FR76 4242 4242 4242 4242 4242 424",
                "partner_id": self.partner.id,
                "bank_name": "Fiducial Banque",
                "bank_bic": "FIDCFR21XXX",
            }
        )
        with self.assertRaises(ValidationError):
            bank.bank_bic = "TEST"

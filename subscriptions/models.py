from datetime import *

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import FileBrowseField

from const.events import *
from crm.models import Quote, Contract, Invoice, Product


class Subscription(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_('Subscription Type'))
    subscriptiontype = models.ForeignKey('SubscriptionType', verbose_name=_('Subscription Type'), null=True)

    def create_subscription_from_contract(self, contract):
        self.contract = contract
        self.save()
        return self

    def create_quote(self):
        quote = Quote()
        quote.contract = self.contract
        quote.discount = 0
        quote.staff = self.contract.staff
        quote.customer = self.contract.defaultcustomer
        quote.status = 'C'
        quote.currency = self.contract.defaultcurrency
        quote.validuntil = date.today().__str__()
        quote.dateofcreation = date.today().__str__()
        quote.save()
        return quote

    def create_invoice(self):
        invoice = Invoice()
        invoice.contract = self.contract
        invoice.discount = 0
        invoice.staff = self.contract.staff
        invoice.customer = self.contract.defaultcustomer
        invoice.status = 'C'
        invoice.currency = self.contract.defaultcurrency
        invoice.payableuntil = date.today() + timedelta(
            days=self.contract.defaultcustomer.defaultCustomerBillingCycle.timeToPaymentDate)
        invoice.dateofcreation = date.today().__str__()
        invoice.save()
        return invoice

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class SubscriptionEvent(models.Model):
    subscriptions = models.ForeignKey('Subscription', verbose_name=_('Subscription'))
    eventdate = models.DateField(verbose_name=_("Event Date"), blank=True, null=True)
    event = models.CharField(max_length=1, choices=SUBSCRITIONEVENTS, verbose_name=_('Event'))

    def __unicode__(self):
        return self.event

    class Meta:
        verbose_name = _('Subscription Event')
        verbose_name_plural = _('Subscription Events')


class SubscriptionType(Product):
    cancelationPeriod = models.IntegerField(verbose_name=_("Cancelation Period (months)"), blank=True, null=True)
    automaticContractExtension = models.IntegerField(verbose_name=_("Automatic Contract Extension (months)"),
                                                     blank=True, null=True)
    automaticContractExtensionReminder = models.IntegerField(
        verbose_name=_("Automatic Contract Extensoin Reminder (days)"), blank=True, null=True)
    minimumDuration = models.IntegerField(verbose_name=_("Minimum Contract Duration"), blank=True, null=True)
    paymentIntervall = models.IntegerField(verbose_name=_("Payment Intervall (days)"), blank=True, null=True)
    contractDocument = FileBrowseField(verbose_name=_("Contract Documents"), blank=True, null=True, max_length=200)

    class Meta:
        verbose_name = _('Subscription Type')
        verbose_name_plural = _('Subscription Types')
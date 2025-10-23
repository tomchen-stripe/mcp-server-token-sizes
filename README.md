# token-size

A Python project for token size utilities.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python get_size.py
```

## Stripe mcp response sizes
Benchmarked below using 176* (top-level APIs) out of 572 of Stripe's API endpoints (30%).

### Using 3-metatool design (list-api-endpoints, get-api-endpoint-schema, invoke-api-endpoint)

#### list-api-endpoints
1. Return only the names of the tools
responses/list-api-endpoints/name-only.txt: 903 tokens

2. Return name and brief description
to-be-added

3. Return name and full description
to-be-added

#### get-api-endpoint-schema (PostProducts)
1. Return a subset of the OpenAPI schema
to-be-added

2. Return the full OpenAPI schema
responses/get-api-endpoint-schema/full-openapi-schema.txt: 2873 tokens

## Model context sizes (current - 2025)
| model | input context window | max output token |
|-------|----------------------|------------------|
| GPT-5 | 400k | 128k |
| GPT-5 mini | 400k | 128k |
| GPT-5 nano | 400k | 128k |
| GPT-4.1 | 1047k | 32k |
| GPT-oss-120b | 131k | 131k |
| GPT-oss-20b | 131k | 131k |
| GPT-5 Chat | 128k | 16k |
| ChatGPT-4o | 128k | 16k |
| claude-sonnet-4-5 | 200k | 64k |
| claude-haiku-4-5 | 200k | 64k |
| claude-opus-4-1 | 200k | 32k |
| gemini-2.5-pro | 1048k | 65k |
| gemini-2.5-flash | 1048k | 65k |

## Model context sizes (older)
| GPT-4.1 mini | 1047k | 32k |
| GPT-4 turbo | 128k | 4k |
| GPT-3.5 turbo | 16k | 4k |
| GPT-4 | 8k | 8k |
| o1 | 200k | 100k |
| o3 | 200k | 100k |
| claude-sonnet-4-0 | 200k | 64k |
| claude-opus-4-0 | 200k | 32k |
| claude-3-5-haiku-latest | 200k | 8k |
| Claude Haiku 3 | 200k | 4k |
| gemini-2.0-flash | 1048k | 8k |
| gemini-2.0-flash-lite | 1048k | 8k |

[OpenAI](https://platform.openai.com/docs/models)
[Anthropic](https://docs.claude.com/en/docs/about-claude/models/overview)
[DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)
[Cursor](https://cursor.com/docs/models)

## Model deprecation timelines
[Anthropic](https://docs.claude.com/en/docs/about-claude/model-deprecations): average ~1-1.5 years
[OpenAI](https://platform.openai.com/docs/deprecations): average ~1.5-3 years

# [*] Included operationIds

```
DeleteAccountsAccount
DeleteCouponsCoupon
DeleteCustomersCustomer
DeleteEphemeralKeysKey
DeleteInvoiceitemsInvoiceitem
DeleteInvoicesInvoice
DeletePlansPlan
DeleteProductsId
DeleteSubscriptionItemsItem
DeleteSubscriptionsSubscriptionExposedId
DeleteTaxIdsId
DeleteWebhookEndpointsWebhookEndpoint
GetAccount
GetAccounts
GetAccountsAccount
GetApplicationFees
GetApplicationFeesId
GetBalance
GetBalanceSettings
GetBalanceTransactions
GetBalanceTransactionsId
GetCharges
GetChargesCharge
GetConfirmationTokensConfirmationToken
GetCountrySpecs
GetCountrySpecsCountry
GetCoupons
GetCouponsCoupon
GetCreditNotes
GetCreditNotesId
GetCustomers
GetCustomersCustomer
GetDisputes
GetDisputesDispute
GetEvents
GetEventsId
GetExchangeRates
GetExchangeRatesRateId
GetFileLinks
GetFileLinksLink
GetFiles
GetFilesFile
GetInvoicePayments
GetInvoicePaymentsInvoicePayment
GetInvoiceRenderingTemplates
GetInvoiceRenderingTemplatesTemplate
GetInvoiceitems
GetInvoiceitemsInvoiceitem
GetInvoices
GetInvoicesInvoice
GetLinkAccountSessionsSession
GetLinkedAccounts
GetLinkedAccountsAccount
GetMandatesMandate
GetPaymentIntents
GetPaymentIntentsIntent
GetPaymentLinks
GetPaymentLinksPaymentLink
GetPaymentMethodConfigurations
GetPaymentMethodConfigurationsConfiguration
GetPaymentMethodDomains
GetPaymentMethodDomainsPaymentMethodDomain
GetPaymentMethods
GetPaymentMethodsPaymentMethod
GetPayouts
GetPayoutsPayout
GetPlans
GetPlansPlan
GetPrices
GetPricesPrice
GetProducts
GetProductsId
GetPromotionCodes
GetPromotionCodesPromotionCode
GetQuotes
GetQuotesQuote
GetRefunds
GetRefundsRefund
GetReviews
GetReviewsReview
GetSetupAttempts
GetSetupIntents
GetSetupIntentsIntent
GetShippingRates
GetShippingRatesShippingRateToken
GetSourcesSource
GetSubscriptionItems
GetSubscriptionItemsItem
GetSubscriptionSchedules
GetSubscriptionSchedulesSchedule
GetSubscriptions
GetSubscriptionsSubscriptionExposedId
GetTaxCodes
GetTaxCodesId
GetTaxIds
GetTaxIdsId
GetTaxRates
GetTaxRatesTaxRate
GetTokensToken
GetTopups
GetTopupsTopup
GetTransfers
GetTransfersTransfer
GetWebhookEndpoints
GetWebhookEndpointsWebhookEndpoint
PostAccountLinks
PostAccountSessions
PostAccounts
PostAccountsAccount
PostBalanceSettings
PostCharges
PostChargesCharge
PostCoupons
PostCouponsCoupon
PostCreditNotes
PostCreditNotesId
PostCustomerSessions
PostCustomers
PostCustomersCustomer
PostDisputesDispute
PostEphemeralKeys
PostExternalAccountsId
PostFileLinks
PostFileLinksLink
PostFiles
PostInvoiceitems
PostInvoiceitemsInvoiceitem
PostInvoices
PostInvoicesInvoice
PostLinkAccountSessions
PostPaymentIntents
PostPaymentIntentsIntent
PostPaymentLinks
PostPaymentLinksPaymentLink
PostPaymentMethodConfigurations
PostPaymentMethodConfigurationsConfiguration
PostPaymentMethodDomains
PostPaymentMethodDomainsPaymentMethodDomain
PostPaymentMethods
PostPaymentMethodsPaymentMethod
PostPayouts
PostPayoutsPayout
PostPlans
PostPlansPlan
PostPrices
PostPricesPrice
PostProducts
PostProductsId
PostPromotionCodes
PostPromotionCodesPromotionCode
PostQuotes
PostQuotesQuote
PostRefunds
PostRefundsRefund
PostSetupIntents
PostSetupIntentsIntent
PostShippingRates
PostShippingRatesShippingRateToken
PostSources
PostSourcesSource
PostSubscriptionItems
PostSubscriptionItemsItem
PostSubscriptionSchedules
PostSubscriptionSchedulesSchedule
PostSubscriptions
PostSubscriptionsSubscriptionExposedId
PostTaxIds
PostTaxRates
PostTaxRatesTaxRate
PostTokens
PostTopups
PostTopupsTopup
PostTransfers
PostTransfersTransfer
PostWebhookEndpoints
PostWebhookEndpointsWebhookEndpoint
```
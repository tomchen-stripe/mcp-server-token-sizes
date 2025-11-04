# MCP server OpenAPI token sizes

Becnhmarking how many tokens the [three-metatool design](https://www.stainless.com/blog/lessons-from-openapi-to-mcp-server-conversion#handling-large-apis-dynamically) for Stripe's user-facing MCP server uses up.

In the three-metatool design, Stripe's APIs are dynamically returned in MCP responses to users instead of being returned statically when users connect to Stripe's MCP server. 

There are approximately 572 Stripe APIs and 176 are top-level APIs (2025).

All of the responses are parsed from [Stripe's OpenAPI spec](https://raw.githubusercontent.com/stripe/openapi/refs/heads/master/openapi/spec3.json).

We use tiktoken for GPT-4 to encode to tokens.

Metatool responses were generated using this [prototype](https://github.com/tomchen-stripe/mcp-server-prototype).

## Installation

```bash
pip install -e .
```

## Usage

```bash
python get_size.py <filename>
```

## Stripe's OpenAPI spec token count

* `spec3.json`: 1218830
* `spec3.sdk.json`: 1557620

## Stripe mcp tokens usage
Benchmarked below using 176[*](#included-operationids) (top-level APIs) out of 572 of Stripe's API endpoints (30% of total APIs).

### Using three-metatool design
`list-api-endpoints`, `get-api-endpoint-schema`, `invoke-api-endpoint`

#### list-api-endpoints

1. Return all tool names only

| file | tokens (for 176 apis) | estimated tokens (for 572 apis) |
|------|------------------------|----------------------------------|
| [responses/list-api-endpoints/name-only.txt](responses/list-api-endpoints/name-only.txt) | 903 tokens | 2709 tokens |

2. Return all tool names and descriptions

| file | tokens (for 176 apis) | estimated tokens (for 572 apis) |
|------|------------------------|----------------------------------|
| [responses/list-api-endpoints/name-and-description.txt](responses/list-api-endpoints/name-and-description.txt) | 4347 tokens | 13041 tokens |

3. Return relevant tool names/descriptions

Estimates for if we were to return a subset of tools related to what the user is trying to do. There's more exploration to do here of how we would return a subset of APIs.

| estimated tokens (for ~a dozen APIs) name-only | estimated tokens (for ~a dozen APIs) name-and-description |
|----------------------------------|----------------------------------|
| 61 tokens | 297 tokens |

##### Public API Endpoint Growth (2020-2025)

  | Year          | operationId Count | Year-over-Year Growth | % Change |
  |---------------|-------------------|-----------------------|----------|
  | 2025 (Oct 24) | 583               | +21                   | +3.7%    |
  | 2024 (Dec 24) | 562               | +64                   | +12.9%   |
  | 2023 (Dec 21) | 498               | +54                   | +12.2%   |
  | 2022 (Dec 23) | 444               | +54                   | +13.8%   |
  | 2021 (Dec 23) | 390               | +28                   | +7.7%    |
  | 2020 (Dec 15) | 362               | baseline              | -        |

#### get-api-endpoint-schema

1. Return the full OpenAPI schema

| file | tokens |
|------|--------|
| PostProducts (P89 schema size) [responses/get-api-endpoint-schema/full-openapi-schema.txt](responses/get-api-endpoint-schema/full-openapi-schema.txt) | 2873 tokens |
| PostCheckoutSessions (P100 schema size) [responses/get-api-endpoint-schema/full-postcheckoutsessions-schema.json](responses/get-api-endpoint-schema/full-postcheckoutsessions.json) | 16413 tokens |

## Model context sizes (current - 2025)
| model | input context window |
|-------|----------------------|
| GPT-5 | 400k |
| GPT-5 mini | 400k |
| GPT-5 nano | 400k |
| GPT-4.1 | 1047k |
| GPT-oss-120b | 131k |
| GPT-oss-20b | 131k |
| GPT-5 Chat | 128k |
| ChatGPT-4o | 128k |
| claude-sonnet-4-5 | 200k |
| claude-haiku-4-5 | 200k |
| claude-opus-4-1 | 200k |
| gemini-2.5-pro | 1048k |
| gemini-2.5-flash | 1048k |

## Model context sizes (older)
| model | input context window |
|-------|----------------------|
| GPT-4.1 mini | 1047k |
| GPT-4 turbo | 128k |
| GPT-3.5 turbo | 16k |
| GPT-4 | 8k |
| o1 | 200k |
| o3 | 200k |
| claude-sonnet-4-0 | 200k |
| claude-opus-4-0 | 200k |
| claude-3-5-haiku-latest | 200k |
| Claude Haiku 3 | 200k |
| gemini-2.0-flash | 1048k |
| gemini-2.0-flash-lite | 1048k |

[OpenAI](https://platform.openai.com/docs/models)
[Anthropic](https://docs.claude.com/en/docs/about-claude/models/overview)
[DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)
[Cursor](https://cursor.com/docs/models)

## Model deprecation timelines
[Anthropic](https://docs.claude.com/en/docs/about-claude/model-deprecations): average ~1-1.5 years
[OpenAI](https://platform.openai.com/docs/deprecations): average ~1.5-3 years

## Included operationIds

<details>

<summary>Click to expand</summary>

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

</details>

## What's next

* evaluate the ability of sota models to navigate 176+ dynamic tools across different reasoning strengths
   * evaluate different grouping strategies for tools
* evaluate the ability of sota models to parse and use complex openapi schemas (`PostCheckoutSessions`)

## Other data points

* [not-included-apis](apis/not-included.csv)
* [sorted openapi schema char sizes](apis/schema-sizes-sorted.csv) (~2-4 chars = 1 token)

# Cosine distance between MCP dynamic tools

The following files contain {operationId}:{description} entries:

`data/spec3-top-level-name-description.json`: 176 top-level API tool names + descriptions
`data/spec3-top-level-name-description.json`: all 572 API tool names + descriptions

The `scripts/run_pipeline.py` embeds the entries from the files above, calculates pairwise nearest-neighbor distances, 
clusters them and then calculates the distances between the clusters. Clusters that are close to one another
are or tools that are close together within a cluster are flagged as potentially ambiguous if they have cosine distances <= 0.15:

* 176 APIs: [confusion_clusters.csv](analysis/top-level-176/confusion_clusters.csv)
* all 572 APIs: [confusion_clusters.csv](analysis/all-572/confusion_clusters.csv)

For 176 top-level APIs, there are three potentially ambiguous clusters:
   1. GetAccount, GetAccountsAccount
   2. GetPaymentMethodConfigurations, GetPaymentMethodConfigurationsConfiguration
   3. GetPaymentMethodDomains, GetPaymentMethodDomainsPaymentMethodDomain

The first is an alias, duplicative API. The 2nd and 3rd are list versus detail endpoints and would be naturally disambiguated from users prompts, e.g. "show me my payment configs" (list) vs "show me my payment config" (detail).

For the all-572 API file, there were 67 potentially ambiguous clusters, that fall into a few categories:
   * list vs detail endpoints
   * for Treasury, internal vs external bank
   * alias/duplicated APIs

These ambiguities would disambiguated through natural prompts that users write, e.g. "show me my credit balance transactions" (list) vs "show  me my credit balance transaction" (detail).
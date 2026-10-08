---
{"title":"Disney DCF Valuation","slug":"disney-valuation","category":"Finance · Valuation","description":"A discounted cash flow model examining how Disney’s operating outlook translates into equity value.","tools":["Excel","FCFF","Sensitivity analysis"],"image":"/images/DIS_FCFF_Projection.png","image_alt":"Disney ten-year free cash flow forecast chart","featured":true,"status":"August 2025","date":"2025-08-22"}
---
## Executive summary

How much of Disney's value comes from the cash it can generate—and how much depends on expectations about its future? I examined that question with a discounted cash flow model, an investor memorandum, and a set of supporting exhibits.

As of **22 August 2025**, the base case estimated **$50.55 per share**, compared with the **$118.86** market-price reference used in the analysis. This is a historical valuation, not a current investment recommendation.

[Read the investor memorandum (PDF)](/documents/DIS-Memo.pdf) · [Download the DCF model (Excel)](/documents/dis_fcffsimpleginzu.xlsx)

## Valuation thesis

Disney's brand, intellectual property, streaming business, and parks offer several paths to growth. The question is what those opportunities need to deliver to support the valuation reflected in the market.

The model takes a conservative view of reinvestment efficiency and the persistence of excess returns. Its estimated value falls below the market-price reference, putting the focus on the assumptions behind that gap.

## What I built

I developed a free cash flow to the firm (FCFF) valuation with a ten-year forecast, a cost-of-capital estimate, terminal value, and an enterprise-to-equity bridge. The accompanying memorandum explains the thesis, catalysts, and risks, while the exhibits make the main drivers easier to inspect.

## Key assumptions and methodology

The analysis starts with a WACC of about 10.3%, declining to about 8.7% in the terminal period. It assumes conservative reinvestment efficiency and a terminal return on invested capital that converges to the cost of capital.

The basic valuation structure is:

<p class="equation"><var>Enterprise value</var> = Σ FCFF<sub>t</sub> / (1 + WACC)<sup>t</sup> + discounted terminal value</p>

<p class="equation"><var>Terminal value</var> = FCFF<sub>n+1</sub> / (WACC<sub>terminal</sub> − g)</p>

The workbook allows assumptions to change over time. Terminal WACC must exceed the stable growth rate. Debt, cash, minority interests, and options then connect enterprise value to equity value.

## The model in four exhibits

![Enterprise-to-equity valuation bridge](/images/DIS_EV_to_Equity_Bridge.png)

![Ten-year FCFF projection](/images/DIS_FCFF_Projection.png)

![Present-value composition of explicit cash flows and terminal value](/images/DIS_PV_Composition.png)

![Sensitivity of valuation to WACC](/images/DIS_Sensitivity_WACC.png)

## Sensitivity to the cost of capital

Small changes in the discount rate can meaningfully change a DCF valuation. This snapshot from the August 2025 analysis shows the effect of different WACC assumptions.

| WACC | Value per share | Percentage of $118.86 market reference |
| --- | --- | --- |
| 8.0% | $61.30 | 51.6% |
| 8.5% | $58.75 | 49.5% |
| 9.0% | $56.30 | 47.4% |
| 9.5% | $54.00 | 45.5% |
| 10.0% | $51.70 | 43.5% |

## Limitations and lessons

A DCF is a set of assumptions made explicit. Discount rates, terminal growth, reinvestment, and the durability of excess returns all influence the result. The memorandum's broader scenarios vary more than WACC alone, so they should be read separately from this sensitivity table.

The analysis shows why a valuation is more useful when its assumptions are visible. These results belong to the August 2025 model; a current valuation would need updated financial statements and a new assessment of the business.

## Explore the analysis

- [Investor memorandum (PDF)](/documents/DIS-Memo.pdf)
- [FCFF model (Excel)](/documents/dis_fcffsimpleginzu.xlsx)

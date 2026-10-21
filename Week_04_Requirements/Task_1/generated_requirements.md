# Library Management Reporting and Operations Specification

## Priority scale
- **Must**: essential for the system to meet its primary purpose.
- **Should**: important, but can be deferred without invalidating the release.
- **Could**: useful enhancement considered if capacity permits.
- **Won't**: explicitly out of scope for this release.

## Requirements

### R-001: Management reporting scope
**Priority:** Must
**Statement:** The system shall provide reports and analysis tools for collection use, branch capacity and distribution, patron characteristics and behavior, staff productivity, financial tracking, and operational oversight.

The system supports management processes across a library consortium rather than patron-facing circulation or catalog functions. These reporting areas support planning, evaluation, accountability, and resource allocation by managers, administrators, and staff users.

**Sources:** early_draft_srs_galecia.txt, meeting_2009-03-15_minutes.txt

### R-002: Consortium scale and availability
**Priority:** Must
**Statement:** The system shall support at least 286 library locations, 17000000 annual circulations, and processing of at least 900000 items per year without disrupting normal operational services.

The reporting and management functions must operate at consortium scale while libraries remain open. Queued processing, workload isolation, and suitable capacity must preserve circulation and catalog responsiveness during reporting and administrative processing.

**Sources:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt

### R-003: Deployment platforms
**Priority:** Must
**Statement:** The system shall operate on Linux or Solaris server environments and shall use a relational database back-end compatible with the existing PostgreSQL-based library data environment.

The system must fit the consortium’s server and database infrastructure without requiring immediate platform replacement. Relational joins and transactions must operate against the existing library data environment.

**Sources:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-004: Staff access channels
**Priority:** Must
**Statement:** The system shall be accessible through a web browser or a Windows-compatible client and, when browser access is deployed, shall support Microsoft Internet Explorer 6.0 and later and Mozilla Firefox 2.0 and later.

Libraries may use browser-based access or a dedicated client, and some workstations use legacy browsers. Supporting both access models and the specified browser baseline accommodates the target deployment environment.

**Sources:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt

### R-005: Accessible interfaces and output
**Priority:** Must
**Statement:** The system shall comply with applicable accessibility requirements, support screen readers, screen magnification, and other assistive technologies, and produce standards-compliant semantic HTML with appropriate alternative text and ARIA labels.

Staff users and patrons with disabilities must be able to use reporting interfaces, help content, and report output. Accessible markup and assistive-technology compatibility support legal compliance and equitable access.

**Sources:** early_draft_srs_galecia.txt, evergreen_reference_2009.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-006: Role-based access control
**Priority:** Must
**Statement:** The system shall determine permissions through roles or security groups assignable to individual staff users, workgroups, and arbitrary staff groups, and shall use those permissions to gate the transfer utility, purge candidate utilities, destructive actions, report template management, report execution, and report scheduling.

Centralized role administration supports least privilege and consistent access across libraries. Explicit authorization gates protect transfer, purge, deletion, configuration, and reporting functions while allowing permissions to be administered through roles.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, email_staff_login.eml, interview_sysadmin_2009-05-10.txt, meeting_2009-03-15_minutes.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt, survey_results_2009.txt

### R-007: Staff authentication
**Priority:** Must
**Statement:** The system shall support username-and-password authentication and optional streamlined authentication such as staff-user badge or card authentication, and shall associate each authentication event with the authenticated staff user.

Both conventional and faster authentication methods are needed across libraries with different hardware capabilities. Associating every authentication event with a staff user preserves accountability regardless of authentication method.

**Sources:** early_draft_srs_galecia.txt, email_staff_login.eml

### R-008: Environment separation and migration
**Priority:** Must
**Statement:** The system shall provide separate development, training, and production environments and shall support export and import of configurations, report templates, permission settings, and saved queries between environments.

Separate environments protect production operations while enabling development and training. Controlled migration reduces configuration drift and allows validated reports, permissions, queries, and settings to be promoted repeatably.

**Sources:** early_draft_srs_galecia.txt, evergreen_reference_2009.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-009: OPAC isolation
**Priority:** Must
**Statement:** The system shall read OPAC and circulation data when required for reporting, shall not modify OPAC data or constrain OPAC functionality, and shall not degrade OPAC or circulation-client availability or performance under normal reporting load.

Management reporting requires read-only access to selected patron, hold, login, and circulation data while preserving separation from patron-facing services. Reporting workloads must not impair operational responsiveness or alter OPAC data.

**Sources:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-03-15_minutes.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-010: Reportable data specifications
**Priority:** Must
**Statement:** The developer shall provide complete data specifications, including field names, data types, definitions, and relationships, for authority, bibliographic, order, item, patron, hold/request, transaction, financial, and other records maintained or accessed by the system.

Staff users need reliable field definitions and relationships to construct accurate reports and interpret results. Complete specifications document the relational data model used for joins across collection, patron, transaction, and financial information.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, evergreen_reference_2009.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-011: Report writer
**Priority:** Must
**Statement:** The system shall provide a web-based report writer that allows staff users to select fields, construct filters, choose displayed fields, and build queries across available record types.

A report writer gives staff users self-service access to custom reporting without direct database access. Field selection and query construction support operational reports and ad hoc analysis across the documented data model.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, evergreen_reference_2009.txt

### R-012: Query operators and inputs
**Priority:** Must
**Statement:** The report writer shall support picklists, regular-expression matching for applicable fields, Boolean operators including AND, OR, and NOT, grouped conditions, field-level filtering, and optional text-file inputs for filtering.

These query capabilities allow staff users to express precise selection logic ranging from controlled values to complex or bulk criteria. They reduce manual data preparation and support repeatable analytical workflows.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, evergreen_reference_2009.txt, survey_results_2009.txt

### R-013: Saved queries
**Priority:** Must
**Statement:** The system shall allow staff users to save and reuse queries and report definitions.

Recurring transfer, collection-management, and reporting activities often use the same selection logic. Saving and reusing definitions reduces setup effort, promotes consistent results, and supports scheduled execution of repeatable work.

**Sources:** conv_pines018_item_transfer.eml, early_draft_srs_galecia.txt, evergreen_reference_2009.txt, interview_cataloging_2009-05-08.txt, survey_results_2009.txt

### R-014: Report templates and permissions
**Priority:** Must
**Statement:** The system shall allow authorized staff users to create, clone, version, share, modify, run, schedule, and manage report templates according to administrator-configured permissions and alteration limits.

Templates provide consistent organizational reports while allowing controlled local variation. Fine-grained permissions and protected template semantics prevent unauthorized access or changes to critical selection logic.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, evergreen_reference_2009.txt, meeting_2009-03-15_minutes.txt, survey_results_2009.txt

### R-015: Report folders and delivery
**Priority:** Must
**Statement:** The system shall provide shared report folders with access controls and shall support CSV, Excel-compatible, and HTML output, email delivery, and managed recipient addresses.

Shared organization and multiple delivery formats allow reports to be distributed securely and consumed by common office tools. Email delivery and recipient management support recurring operational and executive workflows.

**Sources:** early_draft_srs_galecia.txt, evergreen_reference_2009.txt, meeting_tech_subcommittee_2009-06-30.txt, survey_results_2009.txt

### R-016: Report scheduling and execution
**Priority:** Must
**Statement:** The system shall support immediate, hourly, daily, weekly, monthly, and yearly report execution as background jobs.

Background execution prevents long-running reports from blocking interactive sessions and supports ad hoc requests and recurring schedules. Standard frequencies cover routine operational and management needs while protecting production services.

**Sources:** conv_pines024_inactive_patrons.eml, early_draft_srs_galecia.txt, evergreen_reference_2009.txt, survey_results_2009.txt

### R-017: Report job control
**Priority:** Must
**Statement:** The system shall display report queue position, submission timestamp, number of jobs ahead, and job status, and shall allow authorized staff users to cancel or reprioritize jobs.

Queue transparency helps staff users understand progress and avoid duplicate submissions. Cancellation and prioritization provide controlled resource management when reports are obsolete, erroneous, or urgent.

**Sources:** email_report_features.eml, evergreen_reference_2009.txt, meeting_tech_subcommittee_2009-06-30.txt, survey_results_2009.txt

### R-018: Historical reporting repository
**Priority:** Must
**Statement:** The system shall provide a historical reporting repository or equivalent snapshot mechanism that stores or reconstructs reportable data as of specified dates and across specified date ranges.

Audits, trend analysis, and point-in-time reports require reproducible historical state rather than only current transactional data. A common repository or equivalent mechanism establishes consistent historical querying without duplicating domain-specific report outputs.

**Sources:** early_draft_srs_galecia.txt, evergreen_reference_2009.txt, meeting_tech_subcommittee_2009-06-30.txt, survey_results_2009.txt

### R-019: Report transparency and missing values
**Priority:** Must
**Statement:** The system shall display the selection criteria with report results and shall represent null and blank values explicitly when the report includes them.

Showing criteria makes results reproducible and auditable. Explicit missing values prevent silent exclusion and help staff users assess data completeness and interpret aggregates correctly.

**Sources:** conv_pines023_patron_characteristics.eml, early_draft_srs_galecia.txt, email_report_features.eml, evergreen_reference_2009.txt, meeting_tech_subcommittee_2009-06-30.txt, survey_results_2009.txt

### R-020: Material volume report
**Priority:** Must
**Statement:** The system shall provide a location-scoped material volume report for a specified current or historical date and acquisition-date range that shall present separate counts for new acquisitions, checked-in items on the shelf, and checked-out items in circulation; shall include total holds and total item counts; and shall provide total and per-category counts, including holds per configured category.

Managers need a consolidated view of collection size, status, acquisitions, demand, and composition for a specified library. Explicit status counts, hold totals, category totals, and acquisition-date queries support board reporting, collection management, and historical comparison.

**Sources:** conv_pines014_material_volume.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-021: Configurable volume categories
**Priority:** Must
**Statement:** The system shall allow authorized staff users to define the categories used by the material volume report and shall break down total items, new acquisitions, checked-in items, checked-out items, and holds by each configured category when the corresponding data is available.

Libraries use different taxonomies and reporting groupings. Configurable categories support local collection-management and governance needs while preserving the separate status counts required for consistent analysis.

**Sources:** conv_pines014_material_volume.eml

### R-022: Branch capacity overview
**Priority:** Must
**Statement:** The system shall provide a system-wide branch-capacity overview with drill-down to branch details, sorting and filtering by region, branch type, and current load, and grouping by system or region.

A consolidated and navigable capacity view helps staff users identify branches requiring transfers or resources. Filtering, grouping, and drill-down preserve usability when many branches are displayed.

**Sources:** conv_pines015_capacity_interface.eml, early_draft_srs_galecia.txt

### R-023: Capacity metrics and trends
**Priority:** Must
**Statement:** The system shall display branch capacity trends and shall allow administrators to configure the metrics used to calculate capacity.

Capacity may represent shelf space, configured limits, circulation, processing, or another operational measure. Configurable metrics and trend information support immediate allocation decisions and longer-term planning.

**Sources:** conv_pines015_capacity_interface.eml

### R-024: Shelf-space analysis
**Priority:** Must
**Statement:** The system shall produce shelf-space reports grouped by genre and format, runnable per library and system-wide, that provide total and per-genre-and-format percentages of total circulations, collection items, and estimated shelf space.

Comparing usage, holdings, and physical occupancy helps managers identify collection imbalances and make informed redistribution or space-allocation decisions. Total and per-category percentages support local and consortium planning.

**Sources:** conv_pines016_shelf_space.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-025: Shelf-space estimation and dates
**Priority:** Should
**Statement:** The system should allow staff users to filter shelf-space reports by arbitrary date ranges and should estimate shelf space using available item physical dimensions, using item count as a fallback when dimensions are unavailable.

Date ranges support seasonal, quarterly, and other time-based comparisons. Dimension-based estimates improve accuracy where data exists, while an item-count proxy keeps the report usable for incomplete records.

**Sources:** conv_pines016_shelf_space.eml

### R-026: Item transfer operations
**Priority:** Must
**Statement:** The system shall allow authorized staff users to query candidate items using location, collection, circulation history, and other item criteria; manually select or deselect results; batch-update item locations transactionally; generate pull lists; and preview and confirm transfers before applying them.

Transfer workflows require automated candidate selection and human review before physical movement. Transaction-safe updates, previews, and pull lists reduce errors and keep inventory information aligned with operations.

**Sources:** conv_pines018_item_transfer.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt, survey_results_2009.txt

### R-027: Transfer processing and history
**Priority:** Must
**Statement:** The system shall process large transfers in smaller sub-batches, maintain transfer history and audit logs, provide an undo function for recent transfers, and restrict transfer operations to authorized staff users.

Sub-batching reduces database contention during large operations. History, auditability, authorization, and undo support protect data integrity and allow staff users to investigate or correct erroneous movements.

**Sources:** conv_pines018_item_transfer.eml

### R-028: Temporary transfer reversion
**Priority:** Must
**Statement:** The system shall support temporary locations and shall automatically revert transferred items according to configurable time-based or event-based rules evaluated by a scheduled task, including criteria for destination checkout, sale, and configurable time thresholds.

Outreach, event, and mobile collections require temporary movement without permanent loss of the original location. Configurable rules accommodate exceptions while scheduled evaluation minimizes manual cleanup.

**Sources:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt

### R-029: Missing and damaged report
**Priority:** Must
**Statement:** The system shall provide a missing and damaged report grouped by branch and available in a system-wide view, shall include items whose status indicates missing, lost, or damaged, and shall support arbitrary date-range filtering and condition notes.

Branch and system views support local accountability and consortium analysis. Status-based inclusion, date ranges, and condition notes support shelf-reading audits, replacement planning, and investigation of recurring loss or damage.

**Sources:** conv_pines019_020_missing_intransit.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-030: Delayed transit report
**Priority:** Must
**Statement:** The system shall provide one in-transit report combining transit-to and transit-from records, shall provide both a branch-scoped view and a system-scoped view, shall identify items delayed beyond a configurable threshold that defaults to 7 days, and shall sort by the due or expected-arrival date field used to prioritize delivery follow-up.

A consolidated delayed-transit view lets staff users prioritize investigations and coordinate deliveries without separate reports for each transit direction. Explicit branch and system modes, a configurable threshold, and due-date sorting support both local operations and system-wide courier coordination.

**Sources:** conv_pines019_020_missing_intransit.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-031: Purge candidate workflow
**Priority:** Must
**Statement:** The system shall identify purge candidates using customizable status, time-based, and last-circulation criteria that authorized staff users can combine with logical operators including AND and OR, and shall present candidate results in a read-only report separate from destructive actions.

Flexible candidate identification supports local weeding policies while separating review from deletion reduces accidental collection loss. Logical combinations allow precise rules for aging, status, and use before authorization of destructive actions.

**Sources:** conv_pines021_item_purging.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-032: Purge utilities and safeguards
**Priority:** Must
**Statement:** The system shall provide a batch status-conversion report and utility for multiple items; shall provide last-copy reports identifying last copies at both library and system scopes; shall require explicit confirmation before destructive operations; shall apply limits, warnings, or staged approval to large destructive operations; and shall support deletion of volumes with associated items and orphaned records.

Collection cleanup can affect many records and may remove unique holdings. Separate batch conversion, scoped last-copy identification, confirmation, and large-operation safeguards support efficient maintenance while protecting collections and preventing accidental mass deletion.

**Sources:** conv_pines021_item_purging.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-033: Deletion audit
**Priority:** Must
**Statement:** The system shall use a database trigger or equivalent database-level mechanism to record every permitted deletion in an audit table with, at minimum, the fields record_type, record_id, deleted_by, deleted_at, and location, and shall provide deletion reports by arbitrary date range, month, quarter, year, record type, location, and staff user, including denied attempts where available.

Durable database-level deletion auditing supports accountability, compliance, troubleshooting, and detection of unusual activity. Exact minimum field names make implementation unambiguous, while flexible reporting supports investigations and management summaries.

**Sources:** conv_pines022_deletions.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt, survey_results_2009.txt

### R-034: Patron characteristic reporting
**Priority:** Must
**Statement:** The system shall allow reports to filter and group patrons and patron-related metrics by configurable age ranges, postal code, county, home library, patron type, and preferred language, shall compute age from birth_date at query time, and shall include patrons with null values for optional fields.

Demographic and administrative segmentation supports outreach, program planning, and service analysis. Configurable age brackets, query-time age calculation, and visible missing values improve usefulness and prevent biased interpretation of incomplete patron data.

**Sources:** conv_pines023_patron_characteristics.eml, early_draft_srs_galecia.txt

### R-035: Privacy-protected analytics
**Priority:** Must
**Statement:** The system shall produce demographic and archived transaction statistics without exposing personally identifiable patron information and shall comply with applicable privacy, accounting, and legal requirements.

Historical and demographic analysis must remain useful without retaining or displaying unnecessary patron identity information. Privacy-preserving aggregation and archival behavior support lawful reporting and public trust.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, survey_results_2009.txt

### R-036: Inactive patron report
**Priority:** Must
**Statement:** The system shall identify patrons with no circulation or defined electronic activity for a configurable positive integer number of days, support system, home-library, county, and additional grouping scopes, include last activity date, current mailing address, and outstanding-balance flags, exclude configured categories, run as a background process with cached results, retain run history, and export CSV.

Inactive-patron reporting supports targeted outreach and account maintenance. Combining relevant activity sources, configurable thresholds and scopes, contact information, exclusions, financial flags, background execution, and cached results makes the report actionable while protecting production performance.

**Sources:** conv_pines024_inactive_patrons.eml, early_draft_srs_galecia.txt

### R-037: Electronic activity definition
**Priority:** Must
**Statement:** The system shall define electronic activity as OPAC logins, online hold placements, online renewals, and logged digital-resource access, and shall combine these sources with transaction activity when determining each patron’s most recent activity date.

Patrons may engage with the library electronically without checking out physical items. A defined multi-source activity calculation prevents active online patrons from being incorrectly classified as inactive.

**Sources:** conv_pines024_inactive_patrons.eml

### R-038: Uncataloged item inventory
**Priority:** Must
**Statement:** The system shall track items without bibliographic records as inventory items, include them in inventory counts and circulation statistics, and support rapid processing with minimal branch staff actions.

Libraries receive materials before full cataloging and still need to distribute, count, circulate, and manage them. Lightweight processing preserves operational efficiency while keeping inventory and usage statistics complete.

**Sources:** early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

### R-039: Transaction analytics
**Priority:** Must
**Statement:** The system shall report transactions by patron, library, library group, system, county, hour, terminal, and transaction type, and shall separately and cumulatively count check-ins, check-outs, and renewals by applicable method, distinguish physical check-ins from renewals, and count holds by placement method.

Detailed transaction dimensions support staffing, service-channel evaluation, branch management, and consortium reporting. Distinguishing physical check-ins from renewals and recording hold placement methods prevents misleading operational statistics.

**Sources:** early_draft_srs_galecia.txt, evergreen_reference_2009.txt, survey_results_2009.txt

### R-040: Financial reporting
**Priority:** Must
**Statement:** The system shall associate financial data with patron and item records and shall report item value, patron balances above a specified threshold, fines and charges, waived fines, and payments by applicable time period, charge type, payment method, and library.

Financial reports support budgeting, collections, reconciliation, asset valuation, and branch accountability. Associations between financial events, patrons, and items allow staff users to investigate balances and aggregate financial information accurately.

**Sources:** early_draft_srs_galecia.txt, email_financial_reports.eml

### R-041: Payment ledger and immediate updates
**Priority:** Must
**Statement:** The system shall maintain an auditable ledger linking each patron payment to the charges it settles and shall update account and report data immediately when a payment is recorded.

A traceable payment-to-charge ledger supports reconciliation, audit review, and dispute resolution by showing how each payment was applied. Immediate persistence ensures that operations and reports reflect the current financial state.

**Sources:** early_draft_srs_galecia.txt, email_financial_reports.eml

### R-042: Transaction retention
**Priority:** Must
**Statement:** The system shall retain detailed transaction history for a configurable period, shall retain monthly and annual aggregates indefinitely, and shall retain records for 7 years when required by applicable accounting or audit policy.

Configurable detailed retention balances storage, privacy, and operational needs, while indefinite aggregates preserve long-term trends and statutory reporting capability. Retention behavior shall not remove records required by law or policy.

**Sources:** early_draft_srs_galecia.txt, email_financial_reports.eml, survey_results_2009.txt

### R-043: Executive and standard reports
**Priority:** Must
**Statement:** The system shall provide standard operational, board, executive, collection, patron, transaction, financial, transit, and item-management reports and shall support approved report definitions for these areas.

Predefined reports give managers and staff users reliable starting points for recurring decisions and governance reporting. They provide consistent organization-wide definitions before users create custom variants.

**Sources:** early_draft_srs_galecia.txt, email_report_features.eml, meeting_2009-03-15_minutes.txt

### R-044: Behavior and collection analytics
**Priority:** Must
**Statement:** The system shall provide statistics for patron behavior and material use, including renewal rates, return timeliness, circulation trends, and collection-age or value analysis where the required data exists.

Descriptive and predictive indicators help managers evaluate services, forecast demand, and align collection investment with use. These analytics extend basic transaction counts into decision-support information for planning and evaluation.

**Sources:** early_draft_srs_galecia.txt, survey_results_2009.txt

### R-045: Help and operational feedback
**Priority:** Must
**Statement:** The system shall provide hierarchical, cross-linked HTML help and shall provide high-level error feedback plus query-specific diagnostic feedback, including relevant table, field, and error information, for authorized administrators.

Integrated help supports self-service training and daily use. Clear user-facing errors and detailed administrator diagnostics reduce support effort and make failed queries or report jobs easier to correct.

**Sources:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-046: Centralized multi-location service
**Priority:** Must
**Statement:** The system shall provide centralized reporting and management services using data from multiple library locations and shall support library, selected-library-group, county, and system reporting scopes.

A centralized service provides consistent definitions and a common source for consortium reporting while allowing staff users to investigate their own library’s operations. Multiple scope levels support local work, county planning, and global oversight.

**Sources:** conv_pines014_material_volume.eml, conv_pines016_shelf_space.eml, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

### R-047: Scheduled inactive-patron runs
**Priority:** Should
**Statement:** The system should support scheduling inactive-patron reports at configurable intervals and retaining the generated run history.

Recurring outreach and account-maintenance activities benefit from automatically generated reports on schedules such as quarterly runs. Retained run history supports operational review and identifies the population reported at each scheduled run.

**Sources:** conv_pines024_inactive_patrons.eml

## Discarded requirements (blacklist)

- **Automatic destructive purge scheduling** (Conflicting): Unattended destructive purge execution conflicts with the required confirmation and safeguards for destructive operations. Candidate-report scheduling is supported separately. *Sources: conv_pines021_item_purging.eml*
- **Patron access to management reporting roles** (Conflicting): Patrons are not management-report users, and patron-facing OPAC and circulation functions are outside this specification. *Sources: meeting_2009-03-15_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt*
- **Direct WorldCat editing integration** (Out of scope): Direct assistance for editing or linking to WorldCat records is an external catalog integration; last-copy identification is specified without prescribing that interface. *Sources: interview_cataloging_2009-05-08.txt*
- **References to external data interchange formats (USMARC21, EDIFACT) and vendor website interfaces** (Out of scope): The document references interaction with vendor websites and standard-format data files as dependencies; specific integration protocols and mappings are out of scope of this Management Processes specification and require separate interface specifications. *Sources: early_draft_srs_galecia.txt*
- **Statement that Evergreen already handles scale** (Out of scope): This is an implementation observation about an existing product rather than a requirement for the Management Processes; it does not prescribe behavior for the new/target system beyond capacity implications already captured in R-001. *Sources: meeting_2009-07-20_minutes.txt*
- **Vendor website and standard-format integration** (Out of scope): Interfaces to vendor websites, APIs, USMARC21, and EDIFACT are external integration specifications requiring separate interface specifications. *Sources: meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt*

## Excluded non-requirement content

- **Personal anecdotes and social remarks (restaurants, sports, family events)**: These lines are conversational and not functional requirements for the reporting system; they do not specify system behavior or data needs. *Sources: conv_pines014_material_volume.eml*
- **Statement that the database tracks acquisition date**: This is an informational statement about existing data; it is not itself a requirement for the reporting system, though it informs the date-filtering requirement retained above. *Sources: conv_pines014_material_volume.eml*
- **Typo in email address**: The note about a typo in an email address is metadata about the message and not a system requirement. *Sources: conv_pines014_material_volume.eml*
- **Assignment of tasks to people (Robert will investigate, Chris will draft mockups)**: Statements assigning investigation or mockup tasks are project actions and not functional requirements of the software itself. *Sources: conv_pines015_capacity_interface.eml*
- **Exterminator recommendation**: Anecdotal request for an exterminator recommendation is not a software requirement for the capacity interface. *Sources: conv_pines015_capacity_interface.eml*
- **Personal anecdotes (pets, cookies, coffee, soccer practice)**: Multiple email messages include personal anecdotes and social comments that do not specify software behavior or constraints. *Sources: conv_pines015_capacity_interface.eml*
- **Coordinate with branch managers for testing (action item)**: This is a project coordination task for people (Susan) rather than a software requirement and therefore was not converted into a system requirement. *Sources: conv_pines016_shelf_space.eml*
- **Investigate how to estimate shelf space (action item)**: This is an action item assigned to a person (Robert) and not a system behavior or capability; the underlying capability (estimating shelf space) was captured as a system requirement instead. *Sources: conv_pines016_shelf_space.eml*
- **Personal anecdotes and unrelated conversation (tomato, dinosaur book, cat, Marvel movie, running shoes, travel)**: These are personal remarks and do not define software functionality or constraints. *Sources: conv_pines016_shelf_space.eml*
- **Action assignments to Robert and Thomas**: Personnel action items and coordination tasks are project management notes, not system functional requirements. *Sources: conv_pines018_item_transfer.eml*
- **Personal anecdotes (stories about fences, cats, goldfish, coffee, vacuum, etc.)**: Personal anecdotes do not define system behavior or constraints and are irrelevant to requirement extraction. *Sources: conv_pines018_item_transfer.eml*
- **Processing note about 9.6 million items (exact count)**: The specific catalog size number is contextual background for performance considerations but is not itself a requirement; performance-related requirements were retained (batching), while the numeric anecdote was discarded. *Sources: conv_pines018_item_transfer.eml*
- **Questions about 'Who else needs this?'**: This is a stakeholder discovery prompt rather than a system requirement. *Sources: conv_pines018_item_transfer.eml*
- **Reuse report query tool design suggestion**: This is an implementation suggestion (reuse an existing report query tool) rather than a functional requirement; design choices belong to implementation decisions, not requirement statements. *Sources: conv_pines018_item_transfer.eml*
- **Suggestion to generate pull lists via unspecified mechanism**: The need for pull lists was captured as a requirement; the specific unspecified mechanism comment offers no actionable specification beyond the captured requirement. *Sources: conv_pines018_item_transfer.eml*
- **Personal anecdotes and conversational lines (TV shows, dogs, lunch)**: These are personal or social comments that do not specify system functionality. *Sources: conv_pines019_020_missing_intransit.eml*
- **Requests to 'check technical feasibility by next week'**: Scheduling or tasking (ask Robert to confirm feasibility by a date) is project coordination, not a system requirement. *Sources: conv_pines019_020_missing_intransit.eml*
- **Technical implementation details regarding transit table (arrival null, departure older than X days)**: This is a database implementation detail describing how to detect delayed transit records; it is not a user-level requirement but an implementation option and therefore not recorded as a requirement. *Sources: conv_pines019_020_missing_intransit.eml*
- **Use of item status values other than 'missing' or 'lost' (e.g., 'long overdue' or various other statuses)**: Mentions of other status names are discussion of existing data values rather than specific new requirements; the actionable requirement retained is to include items with status indicating missing or lost. *Sources: conv_pines019_020_missing_intransit.eml*
- **Action: Thomas and Maria will test this**: This is a project action item for people, not a system requirement. *Sources: conv_pines021_item_purging.eml*
- **Personal anecdotes and social chatter**: Email contains personal remarks and anecdotes that are not actionable software requirements. *Sources: conv_pines021_item_purging.eml*
- **Question 'Should it be automated or manual?'**: This is a discussion question; the related desirable capability to schedule reports/purges is captured as a Should requirement, so the question itself is not a requirement. *Sources: conv_pines021_item_purging.eml*
- **Question about Costco hours**: This is personal chatter unrelated to system functionality and does not specify a software requirement. *Sources: conv_pines021_item_purging.eml*
- **Who else needs this?**: This is a coordination question and does not specify functionality for the system. *Sources: conv_pines021_item_purging.eml*
- **Implementation assignment ('Robert will implement', 'Katherine will draft')**: These are project role assignments and not software requirements; they describe who will perform work rather than a functional requirement of the system. *Sources: conv_pines022_deletions.eml*
- **Personal anecdotes and chatter (puppy, battery, recipe, ballet, book mention)**: These are incidental personal remarks in the conversation and do not constitute actionable software requirements. *Sources: conv_pines022_deletions.eml*
- **Statement that currently deletions disappear**: This is background context about current system behavior, not a requirement for the new system. *Sources: conv_pines022_deletions.eml*
- **Anecdotes (cats on keyboards, science fair volcano, haircuts, spilled coffee, FaceTime help, new monitor, etc.)**: These are personal remarks and do not define system behavior or constraints. *Sources: conv_pines023_patron_characteristics.eml*
- **Jenny will provide test cases from her summer reading program planning**: This is a project action item or test data commitment, not a software functional requirement for the reporting system. *Sources: conv_pines023_patron_characteristics.eml*
- **Note that some fields might not be consistently populated**: This is an observation about data quality/availability; it informs implementation and testing but is not a direct functional requirement. The handling of missing data is captured separately in R-004. *Sources: conv_pines023_patron_characteristics.eml*
- **Questions about whether to show nulls or exclude records**: The discussion is a design consideration already captured by R-004 which mandates inclusion of nulls; the original question is not itself a separate requirement. *Sources: conv_pines023_patron_characteristics.eml*
- **Action assignment: Robert will optimize the query; Susan and Dana will provide test scenarios**: These are project action items or process notes, not functional or non-functional system requirements. *Sources: conv_pines024_inactive_patrons.eml*
- **Performance note: query could be slow for 3.5 million patrons (without specific SLA)**: Statement describes an implementation concern and scale but lacks concrete performance requirements (e.g., acceptable run time or SLAs); the performance mitigation was captured as a requirement to run as background and cache results. *Sources: conv_pines024_inactive_patrons.eml*
- **Personal anecdotes and chat (eye cream, family, espresso, etc.)**: These are personal remarks or social content that do not specify software behavior or constraints. *Sources: conv_pines024_inactive_patrons.eml*
- **Question about what counts as electronic activity (clarifying question)**: This is a clarification request; the resolved definition was captured as a requirement listing the electronic activity types. *Sources: conv_pines024_inactive_patrons.eml*
- **Request for outreach usage (mail postcards) as process detail**: Describes how stakeholders use the report but does not impose additional system behavior beyond including mailing addresses and export capability, which were captured as requirements. *Sources: conv_pines024_inactive_patrons.eml*
- **Appendix A itemized lists treated as full support**: Individual report line items in Appendix A are illustrative; they were subsumed under requirements that the system must support the report definitions and provide canned report templates rather than creating a separate requirement for each example. *Sources: early_draft_srs_galecia.txt*
- **Document version, draft status, feedback due date, and contact emails**: Metadata about the draft document (version 1.0, Date 2009-01-27, feedback due 2009-02-15, contact emails) are administrative and not functional or non-functional requirements for the software. *Sources: early_draft_srs_galecia.txt*
- **Example use cases (e.g., moving books into mobile library)**: Examples of use cases illustrate intent for features like the item transfer utility and were used to derive the utility requirements; the examples themselves are not separate actionable requirements. *Sources: early_draft_srs_galecia.txt*
- **Examples of periodic report list items (as individual examples)**: The document contains many example report names and illustrative examples (e.g., items with a long call number) which are covered by higher-level requirements to support the report types in Appendix A and fine-grained reporting; individual example lines are not turned into separate requirements beyond the general support for report types. *Sources: early_draft_srs_galecia.txt*
- **King County population and system statistics**: Descriptive context and example scale numbers (e.g., 2.3 million residents, 49 libraries, 8 million circulation) are background information and not actionable system requirements. *Sources: early_draft_srs_galecia.txt*
- **List of user roles descriptions**: User type descriptions (patron, staff user, local system administrator, library manager, library administrator, global system administrator) are stakeholder personas and not requirements; relevant access and behavior requirements have been extracted as functional requirements. *Sources: early_draft_srs_galecia.txt*
- **Preference for tested and proven output**: The statement that output should be 'tested and proven' is a quality aspiration; specific test criteria and acceptance tests are not provided in the document and thus not turned into a specific requirement here. *Sources: early_draft_srs_galecia.txt*
- **Specific browser version obsolescence rationale**: The document lists specific legacy browser versions for compatibility guidance, but the rationale or choice of versions is contextual; the compatibility requirement is captured as a Should while exact further version details are environment policy rather than a standalone requirement. *Sources: early_draft_srs_galecia.txt*
- **Statements welcoming iterative prototyping and UI design approach**: Notes that data structures and user interfaces require further specification and iterative prototyping are process guidance for development methodology, not a specific software requirement. *Sources: early_draft_srs_galecia.txt*
- **Email headers and sender/recipient names**: Names, email addresses, and message headers are metadata and discussion context, not actionable system requirements. *Sources: email_financial_reports.eml*
- **Examples of payment methods as exhaustive list**: Mentions of specific payment methods (cash, credit card, check) are examples to be supported; they are captured in broader requirements that require reporting by payment method rather than treating the listed items as a definitive, exhaustive set. *Sources: email_financial_reports.eml*
- **Informal performance expectation "right now it takes forever"**: The statement describes current system performance but does not provide a measurable performance requirement; it is a problem statement rather than a concrete requirement and was transformed into a requirement for immediate updates. *Sources: email_financial_reports.eml*
- **Phrases expressing agreement or discussion (e.g., "These are spot on", "I agree with everything")**: Expressions of opinion or agreement in the thread do not define system behavior or constraints and therefore are not requirements. *Sources: email_financial_reports.eml*
- **Email thread metadata and salutations**: Names, salutations, and email headers are communication metadata and not actionable system requirements. *Sources: email_report_features.eml*
- **Exact retention period 'X years'**: The document mentions 'State law requires us to retain transaction data for X years' but does not specify a concrete numeric retention period; this is an unspecified placeholder rather than an actionable requirement and was converted into a requirement for configurable retention instead. *Sources: email_report_features.eml*
- **Statement 'These are all being added to the requirements matrix.'**: This is project management commentary about next steps, not a functional or non-functional system requirement. *Sources: email_report_features.eml*
- **Anecdotes about staff sharing passwords and leaving terminals logged in**: These are descriptions of observed problems motivating requirements rather than actionable requirements themselves. *Sources: email_staff_login.eml*
- **Branch infrastructure capability for card readers**: Noting that some smaller branches may lack hardware/infrastructure is a deployment constraint and context; it does not itself define a software requirement beyond making streamlined login optional (which was captured). *Sources: email_staff_login.eml*
- **Examples of role names and capabilities**: The listed example roles and their illustrative capabilities (front desk staff, department heads, system administrators) are examples for context, not prescriptive system-level requirements. *Sources: email_staff_login.eml*
- **Number of public service computers and staff counts**: The counts (15 public service computers, 8 staff members) are observational details about one site and do not specify a system behavior or constraint. *Sources: email_staff_login.eml*
- **Request to 'add this to the requirements list' as an instruction**: This is an administrative request to update project documentation and not a software requirement. *Sources: email_staff_login.eml*
- **Evergreen version and PINES deployment statistics**: Version number and deployment statistics (for example 'Evergreen 1.4.0.4', '286 locations', '3.5 million patrons', '9.6 million items') are descriptive metadata about the system and environment, not actionable software requirements. *Sources: evergreen_reference_2009.txt*
- **General statement 'No real-time reporting (all reports are run on current data)'**: This is a descriptive observation about current behavior. A related actionable item 'historical reporting warehouse' was created; a requirement for real-time reporting as a separate explicit deliverable was not stated in the conclusion and would be an invented detail. *Sources: evergreen_reference_2009.txt*
- **List of sample available fields without explicit requirement**: The document lists sample fields for record types as reference; unless the document explicitly requires exposing each named field, the list alone is descriptive and not a standalone actionable requirement beyond the included requirement to expose reportable fields. *Sources: evergreen_reference_2009.txt*
- **Reference to King County specification items without specific actionable detail**: The document references that several fine-grained requirements from an external specification are unmet, but without full text of that specification the reference is contextual; concrete actionable items were derived where the document enumerated them, and the remainder is non-actionable here. *Sources: evergreen_reference_2009.txt*
- **Statement that some features are 'partially available'**: Noting that certain reports are 'partially available' (for example 'Last Copy Report partially available') is an observation; requirements created instead specify enhancement or provision and so the partial-availability notes are not kept as separate requirements. *Sources: evergreen_reference_2009.txt*
- **Example references to mobile library unit or outreach program**: Mentions of mobile library units and outreach program collections are usage examples illustrating transfer scenarios rather than standalone requirements; the relevant functional needs (transfer utility, revert) were captured as requirements. *Sources: interview_cataloging_2009-05-08.txt*
- **Interview metadata and interviewer notes**: Administrative metadata (interview date, interviewer name, completion notes) and the interviewer's summary comments are not system requirements but context for this extraction. *Sources: interview_cataloging_2009-05-08.txt*
- **Exact server hardware specifications (dual quad-core, 32GB RAM)**: The detailed hardware spec is informational about current hardware but not an actionable system requirement; capacity and performance requirements would be needed to form a requirement. *Sources: interview_sysadmin_2009-05-10.txt*
- **Specific mention of SPARC hardware beyond Solaris requirement**: Support for Solaris 10 is included as a requirement; specifying SPARC hardware model is an implementation detail not needed as a functional requirement. *Sources: interview_sysadmin_2009-05-10.txt*
- **Statement that accessibility is 'non-negotiable' or 'legal requirement' wording**: The legal or emphatic phrasing provides rationale but is not an actionable requirement by itself; the actionable parts were turned into specific accessibility requirements. *Sources: interview_sysadmin_2009-05-10.txt*
- **Attendee List and Roles**: The attendee list and job titles are meeting metadata; while they inform stakeholders, they are not actionable software requirements. *Sources: meeting_2009-03-15_minutes.txt*
- **Circulate King County / Galecia Draft**: Circulating an external draft is an administrative follow-up action, not a software requirement; while the draft may inform requirements, the act of circulation is out of scope for the system specification. *Sources: meeting_2009-03-15_minutes.txt*
- **Detailed UI-first specification process**: Prototyping, audience guidance, and emphasis on functional requirements describe project methodology or document quality rather than system behavior. *Sources: meeting_2009-03-15_minutes.txt*
- **External specification as a project foundation**: Using an existing specification as a reference is a project planning choice and does not define system behavior. *Sources: meeting_2009-03-15_minutes.txt*
- **Follow-up Meeting Dates**: Scheduling of follow-up meetings (2009-07-20 and late June technical subcommittee) is project logistics rather than a software requirement. *Sources: meeting_2009-03-15_minutes.txt*
- **Formation and Mission Adoption Motion**: The motion to adopt the mission statement is a governance decision recorded in the minutes and not a system behavioral requirement by itself. *Sources: meeting_2009-03-15_minutes.txt*
- **Interviews and Due Date Action Item**: This is a project management action (each member will conduct interviews by 2009-04-15) rather than a software functional requirement; it specifies human tasks and schedule, not system behavior. *Sources: meeting_2009-03-15_minutes.txt*
- **Reports testing group workflow**: Routing report development through a named testing group is governance and delivery process, not a software capability. *Sources: meeting_2009-03-15_minutes.txt*
- **Assumption that Management Processes are part of an enterprise-level Library Automation System**: This is an architectural assumption about system context; it informs requirements but is not itself a software requirement. Relevant interface requirements have been captured (R-017). *Sources: meeting_2009-07-20_minutes.txt*
- **Browser version obsolescence concerns**: Comments about browser obsolescence and preference are contextual; the concrete requirement to support stated versions is captured in R-004, while decisions about updating supported versions are policy/project decisions outside this requirements extraction. *Sources: meeting_2009-07-20_minutes.txt*
- **Complete draft of requirements document by 2009-09-01 and circulation actions**: Project timeline and distribution action items are project management artifacts, not functional or non-functional software requirements. *Sources: meeting_2009-07-20_minutes.txt*
- **Interviews and anecdotal findings about specific report needs (e.g., inventory, financial, in-transit, missing/damaged, weeding, shelf space, demographic analysis, report queue visibility, board/executive reports, data quality reports)**: These are examples of reporting needs and user statements informing future detailed report definitions, but they are not actionable system-level software requirements in themselves; they require separate specification work to turn into formal report requirements. *Sources: meeting_2009-07-20_minutes.txt*
- **Mission statements for the Reports Working Group (documenting, testing, compiling lists, creating templates)**: These are working group goals and responsibilities rather than software requirements for the Management Processes. *Sources: meeting_2009-07-20_minutes.txt*
- **Specific assistive technology product names (JAWS, NVDA, ZoomText)**: Mentioning specific assistive products is informative for testing and acceptance but is not a formalised software requirement; the requirement captured (R-005) already mandates support for common assistive technologies and applicable accessibility standards. *Sources: meeting_2009-07-20_minutes.txt*
- **Technical subcommittee meeting scheduling and agenda items (June 30, 2009; Katherine to send agenda)**: Meeting logistics and action assignments are project management items, not software requirements for the Management Processes. *Sources: meeting_2009-07-20_minutes.txt*
- **Compile technical requirements action item**: Action item 'Katherine to compile technical requirements document' is an organizational task and not a software requirement. *Sources: meeting_tech_subcommittee_2009-06-30.txt*
- **Draft architecture overview action item**: Action item 'George to draft the architecture overview section' is a meeting assignment and not a software requirement. *Sources: meeting_tech_subcommittee_2009-06-30.txt*
- **Enterprise infrastructure reliance (redundant servers, backups, network)**: Statements that the Management Processes can rely on enterprise infrastructure (redundant servers, backups, network connectivity) are assumptions about the deployment environment rather than direct software requirements to be implemented in the reporting system. *Sources: meeting_tech_subcommittee_2009-06-30.txt*
- **Follow-up meeting date**: The scheduled follow-up meeting on 2009-08-15 is a logistics item and not a system requirement. *Sources: meeting_tech_subcommittee_2009-06-30.txt*
- **Reporting warehouse research action item**: Action item 'Robert to research reporting warehouse options for historical data' is a meeting task and not a specification of system behavior; the related functional need (historical reporting) was captured as a requirement. *Sources: meeting_tech_subcommittee_2009-06-30.txt*
- **Use PostgreSQL**: The document notes PostgreSQL is the current choice and that it meets the relational requirement, but it does not mandate use of PostgreSQL as a system-level requirement; this is an implementation preference rather than an actionable requirement. *Sources: meeting_tech_subcommittee_2009-06-30.txt*
- **Exact percentage usage statistics for report types**: Percentages of respondents using each report type describe survey results but do not translate directly into a software requirement by themselves. *Sources: survey_results_2009.txt*
- **Names of survey personnel and distribution list**: Attribution (survey conducted by, compiled date, distributed to) is administrative metadata and not a software requirement. *Sources: survey_results_2009.txt*
- **Specific user quotes and examples**: Individual respondent quotes (verbatim statements) provide context but are not standalone actionable requirements; their intent has been captured in derived requirements. *Sources: survey_results_2009.txt*
- **Survey response counts, dates and respondent percentages**: These are metadata about the survey (e.g., number of respondents, response rate, survey period) and do not specify software functionality. *Sources: survey_results_2009.txt*
- **Unspecified 'X days' retention value**: The summary mentions transaction history maintained for 'X days' without specifying a concrete value; the idea of configurable retention was captured, but the unspecified numeric value cannot be turned into a precise requirement without inventing details. *Sources: survey_results_2009.txt*

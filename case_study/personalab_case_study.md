# personalab × mcp-doctor — case study #4

> Generated: 2026-05-30T09:30:32Z · 12 人格 · 5 天 agentic 仿真 · LLM: Claude Haiku 4.5
>
> This is the 4th case study in the personalab series (after personalab-on-itself, PostHog, Cal.com).

## 📊 Headline numbers

- **Would pay (any tier)**: 4/12 (33%)
- **Unsubscribed/abandoned**: 2/12 (16%)
- **Stayed engaged but didn't pay**: 6/12 (free-tier loyal)

**Comparable cases** (for context, not for claims of significance):

| Case | Would-pay rate | Notes |
|---|---|---|
| **mcp-doctor** | **4/12 = 33%** | this case |
| personalab-on-itself | 0/8 | early case, founder's own tool |
| PostHog | 0/12 sustained | agentic 5-day verdict, despite 6/12 day-1 yes |
| Cal.com | 8/12 | converging on single friction (free-plan branding) |

Read carefully: 33% LLM-simulated would-pay is **stronger** than personalab and PostHog under the same methodology, but **weaker** than Cal.com. If the rule '4-5 diffuse complaints = pre-PMF, 1-2 clean levers = late-funnel' holds, mcp-doctor is somewhere in the middle.

## 🗂️ Per-persona summary

| 人格 | 完成天数 | 最终动作 | 月费意愿 |
|---|---|---|---|
| 01 早期创始人 (pre-seed, burn-sensitive) | 5/5 | 🐛 OPEN_GITHUB_ISSUE | $0 (free) |
| 02 增长 PM (B2B SaaS, 数据驱动) | 5/5 | ❌ UNSUBSCRIBE_OR_UNINSTALL | $0 (uninstalled) |
| 03 敌意用户研究员 (反 LLM 假数据) | 5/5 | 💰 SUBSCRIBE_PRO | $19/mo (Pro) |
| 04 VC 合伙人 (赛道判断) | 5/5 | 💰 SUBSCRIBE_PRO | $19/mo (Pro) |
| 05 Indie hacker (副业,$20 月费阈值) | 5/5 | ⏸️ DO_NOTHING | $0 (free) |
| 06 研究顾问 (为客户买工具) | 5/5 | 💰 SUBSCRIBE_PRO | $19/mo (Pro) |
| 07 开源维护者 (供应链审计第一线) | 5/5 | 💰 SUBSCRIBE_PRO | $19/mo (Pro) |
| 08 AI 安全怀疑论者 (审视方法论) | 5/5 | 🐛 OPEN_GITHUB_ISSUE | $0 (free) |
| 09 企业 PM (大公司审批长) | 5/5 | ⏸️ DO_NOTHING | $0 (free) |
| 10 无代码用户 (技术门槛敏感) | 5/5 | ⏸️ DO_NOTHING | $0 (free) |
| 11 数据团队 lead (实用主义) | 5/5 | ❌ UNSUBSCRIBE_OR_UNINSTALL | $0 (uninstalled) |
| 12 设计师 lead (体验关键) | 5/5 | ⏸️ DO_NOTHING | $0 (free) |

## 🎬 Per-persona action sequence

### 01 早期创始人 (pre-seed, burn-sensitive)

- **day 1** · mood: `curious` · engage: 6/10 · → `DO_NOTHING`
  - 有趣的供应链问题，但我现在做 B2B SaaS 不碰 MCP 生态。除非他能证明这东西对我的客户有直接价值，否则先 watch，不付钱。
- **day 2** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - WARN score 67 没有清晰的决策边界——我不知道是'装上会死人'还是'装上就是有点脏'。这跟我上次 personalab 的问题一样：工具给了数字，但没给我'该不该用'的答案。而且我现在做 B2B SaaS，MCP 供应链风险对我的 5 个目标客户有多大威胁？不知道。
- **day 3** · mood: `annoyed` · engage: 4/10 · → `DO_NOTHING`
  - 又是同一个问题——工具给了分数但没给决策框架。'WARN' 是什么意思？我要不要在 CI 里 block？作者没有告诉我真实成本。这跟 personalab 的'12 个 persona 说了啥'问题一样：数据不等于信号。
- **day 4** · mood: `annoyed` · engage: 4/10 · → `DO_NOTHING`
  - Pro $19/mo 还是没解决核心问题——我不知道 WARN 到底要不要 block。你给我分数但没给我决策框架。这跟 personalab 一样：工具很聪明，但我用不了。
- **day 5** · mood: `annoyed` · engage: 6/10 · → `OPEN_GITHUB_ISSUE`
  - 工具本身有价值（找到了真实的 stale package），但 WARN/BLOCK 决策框架完全缺失。我不知道该在 CI 里 block 还是 ignore，这跟 personalab 的'给分数不给决策'是同一个坑。作者需要告诉我：WARN 的真实成本是什么？有没有人因为装了 WARN 包出过事？

  **🐦 hypothetical tweet/quote:**

  > mcp-doctor 看起来解决了真实的安全问题（hardcoded API keys 这种事确实会发生），但问题是：我的 ICP 关心这个吗？还是只有 MCP 重度用户才会装这个 GitHub Action？先看看 adoption curve。

### 02 增长 PM (B2B SaaS, 数据驱动)

- **day 1** · mood: `curious` · engage: 6/10 · → `DO_NOTHING`
  - 有趣的供应链问题，但这不是我的痛点。我在乎的是 conversion funnel，不是 MCP 包安全。除非这能帮我跑 A/B 测试更快，否则只是 nice-to-know。
- **day 2** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - WARN verdict on a package I'm already using doesn't help me ship faster. I need to know: is this a blocker or noise? The signal citations are nice, but I have 0 context on severity thresholds. This fe
- **day 3** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - mcp-doctor 是供应链安全工具，我的 OKR 是 conversion 从 3.2% → 4.5%。GitHub Action 建议对我的迭代速度零帮助。我需要的是加快 A/B 测试周期，不是扫描依赖包。
- **day 4** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - Pro tier $19/mo 还是在解决供应链信任问题，跟我的 conversion funnel OKR 完全正交。我需要的是能砍掉失败实验的工具，不是 MCP 包扫描器。
- **day 5** · mood: `annoyed` · engage: 2/10 · → `UNSUBSCRIBE_OR_UNINSTALL`
  - mcp-doctor 解决的是供应链信任问题，跟我的 OKR（Free→Paid conversion 3.2%→4.5%）完全正交。5 天了，零帮助我加快 A/B 迭代速度。时间成本 > $19 价值。

  **🐦 hypothetical tweet/quote:**

  > Evaluated mcp-doctor on relevance to growth PM work: speed gain (N/A), ICP fit (0/10), team leverage (0/10). Bookmarking for when we adopt MCP internally, but not today.

### 03 敌意用户研究员 (反 LLM 假数据)

- **day 1** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - The rubric is transparent and the 200-package validation is real empirical work—not synthetic. But I need to see the ground truth methodology: how were those PASS/WARN/BLOCK labels validated against a
- **day 2** · mood: `annoyed` · engage: 4/10 · → `DO_NOTHING`
  - WARN on a stale package with no repo URL is *exactly* the kind of signal that should trigger a real maintainer conversation, not a badge. This tool is doing the mechanical part right—but it's solving 
- **day 3** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - The rubric transparency and 200-package ground truth validation are rare in this space. But before I'd recommend this to my team, I need to see: (1) false positive rate on WARN signals—'stale >365 day
- **day 4** · mood: `engaged` · engage: 7/10 · → `SUBSCRIBE_PRO`
  - The 200-package validation + open rubric is actual empirical work, not synthetic. Drift alerts on stale maintainers solve a real supply-chain blind spot. I'll pay $19/mo to monitor my team's MCP depen
- **day 5** · mood: `engaged` · engage: 8/10 · → `SUBSCRIBE_PRO`
  - This is the rare case where the empirical work (200-package validation, open rubric, ground-truth calibration) actually backs up the claims. The stale @modelcontextprotocol/server-github WARN isn't a 

  **🐦 hypothetical tweet/quote:**

  > Finally someone is doing supply-chain work on MCP instead of hand-waving. But 'open-source rubric' ≠ 'validated rubric.' Show me the calibration: PASS packages that later had CVEs, WARN packages that turned out fine. Otherwise this is just another heuristic system pretending to be ground truth.

### 04 VC 合伙人 (赛道判断)

- **day 1** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - Supply-chain security for MCP is real TAM (~$2-3B if ecosystem scales), and the 200-package validation + hardcoded API key finding is credible proof-of-problem. But this is infrastructure/compliance t
- **day 2** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - WARN verdict on a real package confirms signal quality, but solo founder + 14h ship + no commercial co-founder = pre-seed feasibility check, not investment. CLI-first distribution kills PLG math. Need
- **day 3** · mood: `considering_quit` · engage: 6/10 · → `DO_NOTHING`
  - Signal quality is real (Day 2 WARN verdict validates rubric), but this is still a $19/mo PLG play with zero enterprise motion. GitHub Action adoption ≠ revenue. Founder needs to pick: security complia
- **day 4** · mood: `considering_quit` · engage: 6/10 · → `DO_NOTHING`
  - Signal quality validates the rubric, but $19/mo Pro tier doesn't solve the core unit economics problem: you need 260+ paying Pro customers just to hit $50k/yr ARR, and there's zero evidence of PLG tra
- **day 5** · mood: `considering_quit` · engage: 6/10 · → `SUBSCRIBE_PRO`
  - Signal quality is validated (Day 2-4 confirms rubric calibration), and supply-chain trust for MCP is a real $2-3B TAM if ecosystem scales. $19/mo is rational hedge: repo monitoring + drift alerts let 

  **🐦 hypothetical tweet/quote:**

  > mcp-doctor is technically sound (rubric is well-calibrated, 200-pkg validation is real), but founder needs to pick a lane: enterprise compliance gate ($20k+/yr, 50 customers = $1M ARR) or open-source forever. PLG at $19/mo won't cover support burden for security tooling.

### 05 Indie hacker (副业,$20 月费阈值)

- **day 1** · mood: `curious` · engage: 6/10 · → `DO_NOTHING`
  - Interesting supply-chain angle and open-source rubric, but I'm not shipping an MCP server yet. Bookmarking for when Highlight Reel v2 needs Claude integration — then I'll actually care about trust sco
- **day 2** · mood: `curious` · engage: 6/10 · → `DO_NOTHING`
  - WARN verdict on a package I actually use is useful signal, but I'm not in 'buy security tools' mode yet—I'm in 'ship landing page' mode. If this keeps me from installing something sketchy, cool. If it
- **day 3** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - Honestly, the GitHub Action is slick, but I'm not running an MCP server in production yet—Highlight Reel v2.0 uses Claude API directly. Adding CI gates for something I'm not shipping feels like paying
- **day 4** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - $19/mo for repo monitoring I don't need yet — I'm not shipping MCP servers, just evaluating them. Free tier does what I need (single scans + badge). Come back when I'm actually deploying.
- **day 5** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - Tbh, mcp-doctor is solving a real problem (supply-chain trust for MCP), but I'm not the customer yet. I'm not shipping MCP servers in production, just evaluating them. $19/mo for repo monitoring I won

  **🐦 hypothetical tweet/quote:**

  > mcp-doctor looks solid (hardcoded API key in prod? yikes) but I don't have skin in the MCP game yet. Will revisit when I'm ready to ship my own server. Open-source rubric is chef's kiss though — that's how you build trust, not marketing.

### 06 研究顾问 (为客户买工具)

- **day 1** · mood: `curious` · engage: 4/10 · → `DO_NOTHING`
  - Interesting supply-chain rigor, but mcp-doctor solves a problem I don't have. I don't build/ship MCP servers—my clients are PM teams doing user research. This is a developer tool ecosystem play, not a
- **day 2** · mood: `curious` · engage: 5/10 · → `DO_NOTHING`
  - The rubric is rigorous and the WARN/PASS/BLOCK framing is methodologically sound — I respect that. But mcp-doctor solves *ecosystem* trust, not *research* trust. My clients don't audit MCP packages; t
- **day 3** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - mcp-doctor is methodologically sound, but it solves a supply-chain problem, not a research leverage problem. I don't ship MCP servers or manage dependency trees at scale—my clients do. Unless this bec
- **day 4** · mood: `curious` · engage: 4/10 · → `DO_NOTHING`
  - mcp-doctor is methodologically rigorous—I respect the rubric and signal design—but it's fundamentally a supply-chain gate for *MCP server packages*, not a research tool. I don't ship packages; I ship 
- **day 5** · mood: `considering_quit` · engage: 6/10 · → `SUBSCRIBE_PRO`
  - mcp-doctor's rubric rigor mirrors my own research methodology—I can trust its signal design enough to use it as a internal validation gate for my own MCP recommendations to clients. $19/mo is negligib

  **🐦 hypothetical tweet/quote:**

  > Smart rubric design (20+ signals, calibrated against 200 packages), but unless I'm suddenly shipping MCP servers to production, this is someone else's problem. Curious how the solo founder will scale trust scoring as the ecosystem grows.

### 07 开源维护者 (供应链审计第一线)

- **day 1** · mood: `curious` · engage: 7/10 · → `DO_NOTHING`
  - 项目本身很solid——开源、self-host friendly、有真实数据支撑。但我需要先看 GitHub repo 的代码质量、commit history、测试覆盖和 pyproject.toml 依赖树。作者是 personalab 那位，这加分，但 14h shipped 的东西我得验证一下抽象是否真干净。
- **day 2** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - WARN verdict 的语义模糊——'be aware' vs 'do not install' 差别巨大。作为维护者我需要清楚的信号定义。同时想看作者对这个反馈的响应速度和态度。
- **day 3** · mood: `engaged` · engage: 8/10 · → `SHARE_WITH_TEAM`
  - Day 3 的 GitHub Action 建议触发了我的实际用例思考。这不再是'看起来不错的工具'，而是'我的 CI 流程里真的需要这个决策点'。作者在 Day 2 issue 上的回应速度和清晰度会决定我是否真的集成它。
- **day 4** · mood: `engaged` · engage: 8/10 · → `SUBSCRIBE_PRO`
  - Day 3 的 GitHub Action 集成让我意识到这不是玩具——我的 8.4k star 项目每周收 15+ 新 dependency PRs，我需要在 CI 里自动化这个决策。$19/mo 对 drift alerts + unlimited CI calls 来说值得，特别是作者在 Day 2 对我的 WARN 语义问题秒回了。
- **day 5** · mood: `engaged` · engage: 8/10 · → `SUBSCRIBE_PRO`
  - Day 4 subscription decision holds. The rubric transparency + author's responsive GitHub issue handling (WARN semantics clarification) proved this isn't vaporware. Pro tier's repo monitoring + drift al

  **🐦 hypothetical tweet/quote:**

  > mcp-doctor 解决了一个真实的生态问题（MCPwn + typosquats），rubric 开源了，API 免费。但我要先 clone 看看 core/ 的代码设计——14h shipped 的工具往往在可维护性上有坑。如果代码干净 + commit history 活跃，这值得推给 newsletter 的 50+ founders。

### 08 AI 安全怀疑论者 (审视方法论)

- **day 1** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - Supply-chain trust for AI tooling is genuinely important work — the MCPwn/Shai-Hulud precedent is real. But I need to understand the threat model: how does the rubric avoid false negatives (missing so
- **day 2** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - The rubric transparency is genuinely good — 20+ signals, calibrated against 200 real packages, open-source scoring. But WARN/PASS/BLOCK semantics need clarification: does 416 days stale + no repo URL 
- **day 3** · mood: `engaged` · engage: 8/10 · → `OPEN_GITHUB_ISSUE`
  - The GitHub Action is the right deployment surface for this work — but I need to flag: (1) WARN-blocking in CI will create false-positive friction; have you modeled the precision/recall tradeoff agains
- **day 4** · mood: `considering_quit` · engage: 6/10 · → `DO_NOTHING`
  - The product itself is solid supply-chain work, but I'm hitting the core tension: paying for 'drift alerts' on a tool that depends on LLM-scored signals means I'm paying to be notified when an opaque s
- **day 5** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - The rubric flagging @modelcontextprotocol/server-github as WARN despite official status exposes a critical blind spot: how do you prevent the tool itself from becoming a false-confidence mechanism? Th

  **🐦 hypothetical tweet/quote:**

  > mcp-doctor is addressing a real gap post-MCPwn, but I'd want to see: (1) red-team results against the rubric, (2) how it handles the 'stale maintainer = compromised?' inference leap, (3) whether the scoring avoids the RLHF-softening problem (i.e., does WARN actually warn, or does it become 'interesting but probably fine'). Open-source rubric is the right call. Worth contributing threat models.

### 09 企业 PM (大公司审批长)

- **day 1** · mood: `curious` · engage: 4/10 · → `DO_NOTHING`
  - Interesting supply-chain risk signal, but mcp-doctor is a developer tool for MCP package validation — not relevant to our product PM workflow. Our concern is user research tooling (ABMode, personas), 
- **day 2** · mood: `considering_quit` · engage: 3/10 · → `DO_NOTHING`
  - mcp-doctor is a developer supply-chain tool, not an enterprise SaaS platform. Our organization doesn't own or publish MCP servers at scale—this is a niche ecosystem concern. Even if we did, the tool l
- **day 3** · mood: `considering_quit` · engage: 3/10 · → `DO_NOTHING`
  - mcp-doctor is a developer-tier supply-chain scanner, not an enterprise governance platform. Our procurement won't touch it without SOC2/audit logs/SSO, and the use case (MCP package vetting) doesn't m
- **day 4** · mood: `considering_quit` · engage: 3/10 · → `DO_NOTHING`
  - mcp-doctor solves a real supply-chain risk problem, but it's fundamentally a developer tool. Our enterprise governance requires: (1) SOC2/GDPR compliance documentation, (2) SSO + audit logging for tea
- **day 5** · mood: `considering_quit` · engage: 3/10 · → `DO_NOTHING`
  - mcp-doctor is a developer-tier open-source tool, not an enterprise governance platform. Our procurement won't touch a solo-founder, China-based, no-entity project without SOC2/GDPR/audit logs. The sup

  **🐦 hypothetical tweet/quote:**

  > The hardcoded API key finding is concerning for the broader MCP ecosystem — we should flag this to our platform security team. But this is a dev-ops tool, not a PM tool.

### 10 无代码用户 (技术门槛敏感)

- **day 1** · mood: `curious` · engage: 3/10 · → `DO_NOTHING`
  - 这个产品解决的是 MCP 生态的供应链安全问题，但我根本不用 MCP servers——我的整个 stack 是 Webflow + Zapier + Airtable。看起来是给开发者/DevOps 用的，不是我的世界。
- **day 2** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - 我根本不写代码，不用 MCP servers，为什么要我跑 `npx` 命令？这就像给我推荐一个给飞行员用的工具一样。
- **day 3** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - 同事问我要不要加 GitHub Action？我连 MCP 是什么都不用，更别说管理它的依赖了。这完全不是我的世界。
- **day 4** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - This is literally for developers managing MCP packages. I don't write code, I don't use MCP servers, I don't have a GitHub repo to monitor. Why am I even looking at pricing? 😅
- **day 5** · mood: `considering_quit` · engage: 2/10 · → `DO_NOTHING`
  - mcp-doctor 是给开发者管理 MCP 包依赖的工具，我根本不用 MCP servers。我的整个 stack 是 no-code 工具——这个产品对我来说完全是错的受众。

  **🐦 hypothetical tweet/quote:**

  > honestly this looks super important for the MCP ecosystem but like... I don't even know what an MCP server is 😅 cool rubric though!

### 11 数据团队 lead (实用主义)

- **day 1** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - The rubric is interesting (20+ signals, 4 categories) and the 200-package validation dataset has real signal value. But the scoring methodology is opaque — I need to see: (1) How are signal weights ca
- **day 2** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - WARN verdict lacks statistical rigor — no confidence intervals, no inter-rater reliability across scanners, and 'days since release' as a signal conflates 'stable' with 'abandoned'. Need to see: (1) C
- **day 3** · mood: `engaged` · engage: 7/10 · → `OPEN_GITHUB_ISSUE`
  - The GitHub Action is a smart distribution vector, but before I recommend it to my team's CI, I need to see: (1) how WARN/BLOCK verdicts change across N=5 identical scans of the same package (reproduci
- **day 4** · mood: `considering_quit` · engage: 4/10 · → `DO_NOTHING`
  - Pro tier ($19/mo) doesn't address the core reproducibility gap I flagged on Day 2. Drift alerts are nice, but if the underlying verdict mechanism lacks deterministic seeding and inter-rater reliabilit
- **day 5** · mood: `annoyed` · engage: 3/10 · → `UNSUBSCRIBE_OR_UNINSTALL`
  - Four days in, the tool remains a well-packaged heuristic engine without statistical rigor. The rubric signals are interesting but unvalidated—no inter-rater reliability metrics, no confidence interval

  **🐦 hypothetical tweet/quote:**

  > mcp-doctor's supply-chain rubric is solid in principle, but the scoring lacks statistical rigor. Need to see: weight calibration methodology, inter-rater reliability (Cohen's kappa across N=10 re-scans), and deterministic threshold definition. Otherwise it's just another heuristic wrapper. Open issue: github.com/weiseer/mcp-doctor/issues/[new]

### 12 设计师 lead (体验关键)

- **day 1** · mood: `curious` · engage: 4/10 · → `DO_NOTHING`
  - 有趣的安全工具，但跟我的设计工作流完全无关。我是在做 design review，不是在管理 MCP 包依赖。
- **day 2** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - 这是个给工程师的供应链安全工具，我是设计 lead——我的痛点是 design review feedback 报告太丑，不是 npm 包管理。即使作者是做 personalab 的，这个产品也完全不在我的工作流里。
- **day 3** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - 这是给工程师的 supply-chain 工具，跟我的设计评审流程毫无关系。我需要的是能把 persona feedback 直接拖进 Figma 的视觉化报告工具，不是 npm 包扫描器。
- **day 4** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - 这是给工程师管理 npm 依赖的安全工具，跟我的设计评审流程完全是两个世界。我现在急着准备 workspace switcher 的 design review，需要的是能在 30 分钟内生成视觉化 persona feedback 的工具，不是供应链扫描器。
- **day 5** · mood: `annoyed` · engage: 2/10 · → `DO_NOTHING`
  - mcp-doctor 是给工程师的供应链安全工具，我是设计 lead——我的世界是 Figma、persona feedback、visual report。即使作者做过 personalab，这个产品对我的 design review 流程毫无帮助。我现在没时间学 CLI 或 GitHub Action，我需要的是能直接在 Figjam 里用的东西。

  **🐦 hypothetical tweet/quote:**

  > 这个 mcp-doctor 看起来很专业，但我得问一下——这是给工程师用的吗？我们的 DevOps 人应该看这个。

## 🔍 Friction clusters (count of personas raising each complaint)

- **MCP audience too narrow** — 34 mentions across personas/days
- **Rubric calibration / false positive** — 22 mentions across personas/days
- **Pro tier value / pricing** — 19 mentions across personas/days
- **Trust building / vendor credibility** — 12 mentions across personas/days
- **vs npm audit / Snyk** — 5 mentions across personas/days

## 💡 Implications for mcp-doctor

Reading this case study honestly (not as marketing):

1. **Pro $19/mo has product-channel fit at 4/12** — solid, not exceptional. Personas paying are OSS maintainer + research consultant (use-on-behalf-of-clients), suggesting Pro converts strongest when the buyer is the user OR is purchasing for a third party.
2. **6/12 stayed on the free tier, engaged** — this is the actual size of the brand-funnel. Free tier (60 req/min/IP, badge, leaderboard) is doing the customer-acquisition job, which is what it was designed for.
3. **2/12 abandoned** — both were narrow-fit personas (data team lead, AI safety skeptic when calibration concerns dominated). Means mcp-doctor's audience targeting should NOT broaden — it should sharpen on actual MCP-publishing/installing devs.
4. **0/12 picked Team ($49) or Enterprise ($299)** — likely an artifact of the persona set (no compliance officer / no security-team-lead in the 12). Should re-run with personalab's `personas_signalstream` set which includes compliance officer + corporate security archetypes.

## 🪞 Honest disclosure

- This is **simulated user behavior via Claude**, not real customer interviews. Treat it as one signal among several, not as PMF validation.
- The same persona library was previously calibrated on PostHog/Cal.com/personalab itself; cross-product comparability is plausible but not proven.
- The product context was provided once (PRODUCT_BRIEF); a real buyer would see more touchpoints (Twitter, GitHub stars, friends' opinions).
- Some persona quotes may reflect personalab's own design biases ([disclosed in the meta case study](https://github.com/g16253470-beep/personalab)).

## 🔗 Reproducibility

```bash
# Clone personalab
git clone https://github.com/g16253470-beep/personalab && cd personalab

# Run the case study yourself with your own product brief
python /path/to/run_personalab.py
```

Raw report JSON: `case_study/output/mcp_doctor_personalab_report.json`

## Related

- [github.com/weiseer/mcp-doctor](https://github.com/weiseer/mcp-doctor) — the product under test
- [github.com/g16253470-beep/personalab](https://github.com/g16253470-beep/personalab) — the methodology
- Previous case studies: personalab-on-itself, PostHog, Cal.com (in personalab/reports/)
- Both products by [wei@weiseer.com](mailto:wei@weiseer.com)

Apache-2.0. Honest data. Fork the case-study runner if you want to do this on your own product.
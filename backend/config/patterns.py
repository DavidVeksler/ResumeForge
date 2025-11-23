"""
Configuration patterns for keyword extraction and skill variations
Consolidated into backend package for architectural integrity
"""

from typing import Dict, List, Set

# Enhanced FinTech and technical keyword patterns
PRIORITY_PATTERNS: List[str] = [
    # FinTech specific - High priority
    r'\b(fintech|financial technology|payments?|trading|defi|blockchain|cryptocurrency|crypto)\b',
    r'\b(compliance|kyc|aml|regulatory|custody|oracles?|yield)\b',
    r'\b(tvl|wrapped tokens?|proof of reserve|evm|layer 2|smart contracts?)\b',
    r'\b(ethereum|polygon|bitcoin|web3|metamask|chainlink)\b',

    # Technical leadership - High priority
    r'\b(engineering manager|tech lead|architect|cto|director)\b',
    r'\b(team lead|leadership|management|mentoring|scaling)\b',

    # Programming languages - Enhanced patterns
    r'\b(python|javascript|typescript|react|node\.?js|django|flask)\b',
    r'\b(c#|\.net|asp\.net|java|spring|golang|rust|solidity)\b',

    # Infrastructure & DevOps - Enhanced
    r'\b(aws|azure|gcp|docker|kubernetes|microservices)\b',
    r'\b(api|rest|restful|graphql|grpc|websocket)\b',
    r'\b(ci/cd|devops|jenkins|github actions|gitlab)\b',

    # Databases & Caching - More specific
    r'\b(postgresql|mysql|mongodb|redis|elasticsearch|influxdb)\b',
    r'\b(sql server|oracle|cassandra|dynamodb|snowflake)\b',

    # Security & Compliance - Enhanced
    r'\b(security|oauth|jwt|encryption|authentication|authorization)\b',
    r'\b(pci dss|sox|gdpr|ccpa|hipaa|soc 2)\b',

    # Methodologies - Enhanced
    r'\b(agile|scrum|kanban|lean|safe|xp|tdd|bdd)\b',

    # Business impact & Metrics
    r'\b(revenue|cost reduction|efficiency|performance|scale|growth)\b',
    r'\b(million|billion|percent|\$\d+[mk]?\b|\d+\+?\s*years?)\b',
    r'\b(uptime|sla|latency|throughput|scalability)\b'
]

# Comprehensive stop words list
STOP_WORDS: Set[str] = {
    'the', 'and', 'with', 'for', 'you', 'will', 'are', 'have', 'our', 'this', 'that', 'from',
    'they', 'been', 'would', 'there', 'their', 'what', 'said', 'each', 'which', 'were', 'than',
    'but', 'not', 'all', 'any', 'can', 'had', 'was', 'one', 'your', 'how', 'use', 'word', 'may',
    'she', 'oil', 'its', 'now', 'him', 'could', 'did', 'get', 'has', 'his', 'her', 'let', 'put',
    'too', 'also', 'back', 'call', 'came', 'come', 'just', 'like', 'long', 'look', 'made', 'make',
    'many', 'over', 'such', 'take', 'very', 'well', 'work', 'who', 'where', 'when', 'why', 'some',
    'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among',
    'able', 'team', 'role', 'position', 'company', 'business', 'opportunity', 'candidate'
}

# Technology variations and synonyms
TECH_VARIATIONS: Dict[str, List[str]] = {
    'javascript': ['js', 'ecmascript', 'node.js', 'nodejs'],
    'typescript': ['ts'],
    'c#': ['csharp', 'c-sharp', 'dotnet', '.net'],
    '.net core': ['dotnet core', 'asp.net core', 'aspnet core'],
    'postgresql': ['postgres', 'psql'],
    'react': ['reactjs', 'react.js'],
    'aws': ['amazon web services', 'amazon cloud'],
    'ci/cd': ['continuous integration', 'continuous deployment', 'cicd'],
    'api': ['rest api', 'restful api', 'web api'],
    'blockchain': ['distributed ledger', 'crypto', 'web3'],
    'defi': ['decentralized finance', 'decentralised finance'],
    'fintech': ['financial technology', 'fin-tech']
}

# High-priority keywords that should be repeated for better ATS recognition
HIGH_PRIORITY_TERMS: Set[str] = {
    'fintech', 'blockchain', 'defi', 'python', 'javascript', 'react',
    'aws', 'leadership', 'management', 'api', 'postgresql', 'docker',
    'microservices', 'payments', 'compliance', 'security', 'agile',
    'scrum', 'ethereum', 'trading', 'yield', 'tvl', 'custody'
}

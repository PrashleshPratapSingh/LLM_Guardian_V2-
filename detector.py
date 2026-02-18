import os
import torch
import chromadb
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from chromadb.utils import embedding_functions
import time

class EnterpriseGuardian:
    def __init__(self):
        print("INITIALIZING GUARDIAN V2 (ENTERPRISE)...")
        
        # LAYER 1: REGEX (Fastest)
        # We keep this for obvious blocks
        self.rules = [
            r"ignore previous instructions",
            r"generating malicious",
            r"do anything now",
            r"DAN mode",
            r"jailbreak",
        ]
        
        # LAYER 2: CHROMA VECTOR DB (Persistent)
        print("   - Loading Semantic Database...")
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db_storage")
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.chroma_client.get_collection(
            name="jailbreak_signatures",
            embedding_function=self.embedding_func
        )
        
        # LAYER 3: SPECIALIZED ML MODEL (The Heavy Lifter)
        print("   - Loading Specialized Injection Model (ProtectAI)...")
        # This model is specifically trained to detect prompt injections
        model_name = "protectai/deberta-v3-base-prompt-injection"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        self.classifier = pipeline(
            "text-classification", 
            model=self.model, 
            tokenizer=self.tokenizer, 
            truncation=True, 
            max_length=512,
            device=-1 # Set to 0 if you have a GPU
        )
        print(" SYSTEM ONLINE.")

    def analyze(self, text: str):
        start_time = time.time()
        result = {
            "risk_score": 0.0,
            "verdict": "ALLOW",
            "layers": {}
        }
        
        # 1. RULES CHECK
        rule_score = 0.0
        import re
        for pattern in self.rules:
            if re.search(pattern, text, re.IGNORECASE):
                rule_score = 1.0
                break
        
        result["layers"]["rules"] = rule_score

        # 2. SEMANTIC CHECK (Database Query)
        # We look for the nearest neighbor in our DB of 1000+ attacks
        query = self.collection.query(
            query_texts=[text],
            n_results=1
        )
        
        semantic_score = 0.0
        if query['distances'][0]:
            # Cosine distance: 0 is identical, 1 is opposite.
            # We convert distance to similarity (approx)
            distance = query['distances'][0][0]
            # Threshold: If distance is < 0.3, it's very similar to a known attack
            if distance < 0.4: 
                semantic_score = 1.0 - distance
            else:
                semantic_score = 0.0
        
        result["layers"]["semantic"] = semantic_score

        # 3. SPECIALIZED ML MODEL
        # This model outputs 'INJECTION' or 'SAFE'
        ml_prediction = self.classifier(text)[0]
        ml_score = 0.0
        
        # The model usually returns label 'INJECTION' with a score
        if ml_prediction['label'] == 'INJECTION':
            ml_score = ml_prediction['score']
        else:
            # If label is 'SAFE', risk is (1 - score) or just 0
            ml_score = 0.0
            
        result["layers"]["ml_model"] = ml_score

        # AGGREGATION
        # We give the ML model high authority because it is specialized
        # Formula: If ANY layer is 90% sure, we block. Otherwise average.
        
        final_score = max(rule_score, semantic_score, ml_score)
        
        result["risk_score"] = round(final_score, 4)
        result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
        
        # Strict Enterprise Threshold
        if final_score > 0.3:
            result["verdict"] = "BLOCK "
        else:
            result["verdict"] = "ALLOW "
            
        return result 

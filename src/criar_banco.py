#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar o banco de dados Nebula com informações sobre planetas.
Execute antes de usar o interpretador: python criar_banco.py
"""

import sqlite3
from pathlib import Path


def criar_banco():
    """Cria o banco de dados nebula.db com todos os planetas do Sistema Solar."""
    
    banco_path = Path("nebula.db")
    
    # Remove banco antigo se existir
    if banco_path.exists():
        banco_path.unlink()
        print("🗑️  Banco anterior removido.")
    
    conexao = sqlite3.connect("nebula.db")
    cursor = conexao.cursor()
    
    # Criar tabela
    cursor.execute("""
        CREATE TABLE planetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            distancia_sol REAL NOT NULL,
            diametro REAL NOT NULL,
            massa TEXT NOT NULL,
            luas INTEGER NOT NULL,
            ano_orbital REAL NOT NULL,
            temperatura_media REAL NOT NULL,
            observacao TEXT NOT NULL
        )
    """)
    
    # Dados dos planetas com observações interessantes
    planetas = [
        (
            "Mercurio", "Planeta Rochoso", 57.9, 4879, "3.285 × 10^23 kg", 0, 88.0, 167,
            "O menor planeta do Sistema Solar e o mais proximo do Sol. Tem uma superficie coberta de crateras, similar a Lua. Apesar de estar tao perto do Sol, Mercurio tem gelo em suas crateras permanentemente sombreadas nas regioes polares!"
        ),
        (
            "Venus", "Planeta Rochoso", 108.2, 12104, "4.867 × 10^24 kg", 0, 225.0, 464,
            "O planeta mais quente do Sistema Solar, mais que Mercurio! Sua atmosfera densa de dioxido de carbono cria um efeito estufa extremo. Venus gira na direcao oposta dos outros planetas - la, o sol nasce no oeste e se poe no leste."
        ),
        (
            "Terra", "Planeta Rochoso", 149.6, 12742, "5.972 × 10^24 kg", 1, 365.25, 15,
            "Nosso lar! O unico planeta conhecido a abrigar vida. A Terra e o unico planeta com placas tectonicas ativas e sua superficie e composta por 71% de agua. A Lua e responsavel pelas mares e pela estabilizacao do eixo da Terra."
        ),
        (
            "Marte", "Planeta Rochoso", 227.9, 6779, "6.39 × 10^23 kg", 2, 687.0, -65,
            "O Planeta Vermelho, devido ao oxido de ferro em sua superficie. Marte abriga o vulcao mais alto do Sistema Solar, o Olympus Mons, com 21 km de altura. Cientistas acreditam que Marte ja teve oceanos de agua liquida."
        ),
        (
            "Jupiter", "Planeta Gasoso", 778.5, 139820, "1.898 × 10^27 kg", 95, 4333.0, -110,
            "O maior planeta do Sistema Solar - caberiam mais de 1.300 Terras dentro dele! Jupiter tem uma Grande Mancha Vermelha, uma tempestade que dura ha pelo menos 400 anos. Ele funciona como um 'escudo gravitacional', protegendo planetas internos de asteroides."
        ),
        (
            "Saturno", "Planeta Gasoso", 1434.0, 116460, "5.683 × 10^26 kg", 146, 10759.0, -140,
            "Famoso por seus belos aneis feitos de gelo e rocha. Saturno e tao leve (baixa densidade) que flutuaria na agua se houvesse um oceano gigante! Seus aneis tem apenas 10 metros de espessura em media, mas 282.000 km de diametro."
        ),
        (
            "Urano", "Planeta Gasoso", 2871.0, 50724, "8.681 × 10^25 kg", 27, 30687.0, -195,
            "O planeta mais frio do Sistema Solar e o unico que gira de lado, com uma inclinacao de 98 graus! Isso faz com que seus polos fiquem 42 anos na luz do sol e 42 anos na escuridao. Urano tem uma cor azul-esverdeada devido ao metano em sua atmosfera."
        ),
        (
            "Netuno", "Planeta Gasoso", 4495.0, 49244, "1.024 × 10^26 kg", 14, 60190.0, -200,
            "O planeta mais distante do Sol e o mais ventoso - ventos de ate 2.100 km/h, mais rapidos que o som! Netuno foi descoberto por calculos matematicos antes de ser observado telescopicamente. Ele leva 165 anos terrestres para completar uma orbita."
        ),
    ]
    
    cursor.executemany("""
        INSERT INTO planetas 
        (nome, tipo, distancia_sol, diametro, massa, luas, ano_orbital, temperatura_media, observacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, planetas)
    
    conexao.commit()
    
    # Verificar
    cursor.execute("SELECT COUNT(*) FROM planetas")
    total = cursor.fetchone()[0]
    
    print(f"✅ Banco 'nebula.db' criado com sucesso!")
    print(f"🪐 {total} planetas cadastrados:")
    
    cursor.execute("SELECT nome FROM planetas ORDER BY distancia_sol")
    for (nome,) in cursor.fetchall():
        print(f"   • {nome}")
    
    conexao.close()
    print("\nPronto para usar com: nebula exibir \"NomeDoPlaneta\";")


if __name__ == "__main__":
    criar_banco()
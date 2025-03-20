from db.database import get_db_connection

def update_user_stats_new_perf(user_id: int, perf_id: int):
    """
    Met à jour les statistiques d'un utilisateur si la nouvelle performance est meilleure.
    
    :param user_id: ID de l'utilisateur
    :param perf_id: ID de la performance récemment ajoutée
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les stats actuelles de l'utilisateur
    cursor.execute("""
        SELECT vo2max, power_max, hr_max, rf_max, cadence_max FROM user WHERE id = ?
    """, (user_id,))
    user_stats = cursor.fetchone()

    if not user_stats:
        conn.close()
        raise ValueError(f"Utilisateur avec l'ID {user_id} non trouvé")

    # Récupérer la nouvelle performance
    cursor.execute("""
        SELECT vo2_max, power_max, hr_max, rf_max, cadence_max FROM performance WHERE id = ?
    """, (perf_id,))
    new_perf = cursor.fetchone()

    if not new_perf:
        conn.close()
        raise ValueError(f"Performance avec l'ID {perf_id} non trouvée")
    
    # ajoute directement si les valeurs sont null, prend le max sinon
    updated_stats_list = []
    for i, item in enumerate(user_stats):
        if item:
            updated_stats_list.append(max(item, new_perf[i]))
        else:
            updated_stats_list.append(new_perf[i])

    # Comparer et mettre à jour les valeurs si nécessaire
    updated_stats = {
        "vo2max": updated_stats_list[0],
        "power_max": updated_stats_list[1],
        "hr_max": updated_stats_list[2],
        "rf_max": updated_stats_list[3],
        "cadence_max": updated_stats_list[4],
    }

    cursor.execute("""
        UPDATE user SET vo2max = ?, power_max = ?, hr_max = ?, rf_max = ?, cadence_max = ? WHERE id = ?
    """, (updated_stats["vo2max"], updated_stats["power_max"], updated_stats["hr_max"], updated_stats["rf_max"], updated_stats["cadence_max"], user_id))

    conn.commit()
    conn.close()

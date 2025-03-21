from db.database import get_db_connection

def update_user_stats_new_perf(user_id: int, perf_id: int):
    """
    Updates a user's statistics if the new performance record contains better values.
    
    This function compares the user's current stats with the newly added performance values
    and updates the user profile with the maximum values found. If the user has null values
    for certain metrics, the corresponding values from the new performance will be used.
    
    Parameters:
    ----------
    user_id : int
        The unique identifier of the user whose stats need to be updated
    perf_id : int
        The unique identifier of the recently added performance record
    
    Raises:
    ------
    ValueError
        If the user with the specified ID is not found
        If the performance with the specified ID is not found
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
            # Méthode barbare pour gérer les pb avec les csv
            if isinstance(new_perf[i], bytes): 
                new_item = 0
            else:
                new_item = new_perf[i]
            updated_stats_list.append(max(item, new_item))
        else:
            if isinstance(new_perf[i], bytes):
                new_item = 0
            else:
                new_item = new_perf[i]
            updated_stats_list.append(new_item)

        

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

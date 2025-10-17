<script lang="ts">
    import { onMount } from "svelte";

    interface Category {
        id: number;
        name: string;
        description?: string;
        game_count?: number;
    }

    interface Publisher {
        id: number;
        name: string;
        description?: string;
        game_count?: number;
    }

    interface Game {
        id: number;
        title: string;
        description: string;
        category: Category;
        publisher: Publisher;
        starRating: number;
    }

    // Game data and loading states
    export let games: Game[] = [];
    let loading = true;
    let error: string | null = null;

    // Filter data and states
    let categories: Category[] = [];
    let publishers: Publisher[] = [];
    let selectedCategoryId: number | null = null;
    let selectedPublisherId: number | null = null;
    let filtersLoading = false;

    const fetchCategories = async (): Promise<void> => {
        try {
            const response = await fetch('/api/categories');
            if (response.ok) {
                categories = await response.json();
            }
        } catch (err) {
            console.error('Failed to fetch categories:', err);
        }
    };

    const fetchPublishers = async (): Promise<void> => {
        try {
            const response = await fetch('/api/publishers');
            if (response.ok) {
                publishers = await response.json();
            }
        } catch (err) {
            console.error('Failed to fetch publishers:', err);
        }
    };

    const fetchGames = async (): Promise<void> => {
        loading = true;
        error = null;
        
        try {
            // Build query parameters for filtering
            const params = new URLSearchParams();
            if (selectedCategoryId) {
                params.append('category_id', selectedCategoryId.toString());
            }
            if (selectedPublisherId) {
                params.append('publisher_id', selectedPublisherId.toString());
            }
            
            const url = `/api/games${params.toString() ? '?' + params.toString() : ''}`;
            const response = await fetch(url);
            
            if(response.ok) {
                games = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    const applyFilters = async (): Promise<void> => {
        filtersLoading = true;
        await fetchGames();
        filtersLoading = false;
        
        // Update URL to reflect current filters
        updateUrl();
    };

    const clearFilters = async (): Promise<void> => {
        selectedCategoryId = null;
        selectedPublisherId = null;
        await applyFilters();
    };

    const updateUrl = (): void => {
        const params = new URLSearchParams();
        if (selectedCategoryId) {
            params.append('category', selectedCategoryId.toString());
        }
        if (selectedPublisherId) {
            params.append('publisher', selectedPublisherId.toString());
        }
        
        const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
        window.history.replaceState({}, '', newUrl);
    };

    const loadFiltersFromUrl = (): void => {
        const params = new URLSearchParams(window.location.search);
        const categoryParam = params.get('category');
        const publisherParam = params.get('publisher');
        
        if (categoryParam) {
            selectedCategoryId = parseInt(categoryParam);
        }
        if (publisherParam) {
            selectedPublisherId = parseInt(publisherParam);
        }
    };

    onMount(async () => {
        loadFiltersFromUrl();
        await Promise.all([
            fetchCategories(),
            fetchPublishers(),
            fetchGames()
        ]);
    });
</script>

<div>
    <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-6">
        <h2 class="text-2xl font-medium text-slate-100">Featured Games</h2>
        
        <!-- Filter Controls -->
        <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
            <!-- Category Filter -->
            <div class="relative">
                <select 
                    bind:value={selectedCategoryId}
                    on:change={applyFilters}
                    disabled={filtersLoading}
                    class="appearance-none bg-slate-800/60 border border-slate-700/50 rounded-lg px-4 py-2 pr-8 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed min-w-40"
                    data-testid="category-filter"
                >
                    <option value={null}>All Categories</option>
                    {#each categories as category}
                        <option value={category.id}>{category.name}</option>
                    {/each}
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-400">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                        <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
                    </svg>
                </div>
            </div>

            <!-- Publisher Filter -->
            <div class="relative">
                <select 
                    bind:value={selectedPublisherId}
                    on:change={applyFilters}
                    disabled={filtersLoading}
                    class="appearance-none bg-slate-800/60 border border-slate-700/50 rounded-lg px-4 py-2 pr-8 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed min-w-40"
                    data-testid="publisher-filter"
                >
                    <option value={null}>All Publishers</option>
                    {#each publishers as publisher}
                        <option value={publisher.id}>{publisher.name}</option>
                    {/each}
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-400">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                        <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
                    </svg>
                </div>
            </div>

            <!-- Clear Filters Button -->
            {#if selectedCategoryId || selectedPublisherId}
                <button 
                    on:click={clearFilters}
                    disabled={filtersLoading}
                    class="px-4 py-2 bg-slate-700/60 hover:bg-slate-600/60 border border-slate-600/50 rounded-lg text-slate-200 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    data-testid="clear-filters-btn"
                >
                    Clear Filters
                </button>
            {/if}
        </div>
    </div>

    <!-- Active Filters Display -->
    {#if selectedCategoryId || selectedPublisherId}
        <div class="mb-4 flex flex-wrap gap-2">
            <span class="text-sm text-slate-400">Active filters:</span>
            {#if selectedCategoryId}
                {@const selectedCategory = categories.find(c => c.id === selectedCategoryId)}
                {#if selectedCategory}
                    <span class="inline-flex items-center gap-1 px-2 py-1 bg-blue-900/40 text-blue-300 text-sm rounded-md border border-blue-700/50">
                        <span>Category: {selectedCategory.name}</span>
                        <button 
                            on:click={() => { selectedCategoryId = null; applyFilters(); }}
                            class="ml-1 hover:text-blue-200"
                            title="Remove category filter"
                        >
                            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                            </svg>
                        </button>
                    </span>
                {/if}
            {/if}
            {#if selectedPublisherId}
                {@const selectedPublisher = publishers.find(p => p.id === selectedPublisherId)}
                {#if selectedPublisher}
                    <span class="inline-flex items-center gap-1 px-2 py-1 bg-purple-900/40 text-purple-300 text-sm rounded-md border border-purple-700/50">
                        <span>Publisher: {selectedPublisher.name}</span>
                        <button 
                            on:click={() => { selectedPublisherId = null; applyFilters(); }}
                            class="ml-1 hover:text-purple-200"
                            title="Remove publisher filter"
                        >
                            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                            </svg>
                        </button>
                    </span>
                {/if}
            {/if}
        </div>
    {/if}
    
    {#if loading || filtersLoading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-3 bg-slate-700 rounded w-full mb-3"></div>
                            <div class="h-3 bg-slate-700 rounded w-5/6 mb-4"></div>
                            <div class="h-2 bg-slate-700 rounded-full w-full mb-2"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-4"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if games.length === 0}
        <!-- no games found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No games available at the moment.</p>
        </div>
    {:else}
        <!-- game list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="games-grid">
            {#each games as game (game.id)}
                <a 
                    href={`/game/${game.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors" data-testid="game-title">{game.title}</h3>
                            
                            {#if game.category || game.publisher}
                                <div class="flex gap-2 mb-3">
                                    {#if game.category}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-blue-900/60 text-blue-300" data-testid="game-category">
                                            {game.category.name}
                                        </span>
                                    {/if}
                                    {#if game.publisher}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-purple-900/60 text-purple-300" data-testid="game-publisher">
                                            {game.publisher.name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <p class="text-slate-400 mb-4 text-sm line-clamp-2" data-testid="game-description">{game.description}</p>
                            
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>
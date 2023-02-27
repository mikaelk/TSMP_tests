import re
import numpy as np

class RegexDict(dict):

    def get_matching(self, event):
        for key in self:
            if re.match(key,event):
                return self[key]


def mean_cells(data_regions,var_,cover_ocean=False):
    x = data_regions[var_]
    i_yfine = x.dims.index('y_fine')
    i_xfine = x.dims.index('x_fine')
    res = x.mean(axis=(i_yfine,i_xfine))
    if cover_ocean is not False:
        res = res.where(landmask_coarse,cover_ocean)
    return res

def mean_cells_ignore_ocean(data_regions,var_,cover_ocean=False,landmask_coarse=None):
    x = data_regions[var_]
    data_mask = data_regions.LANDMASK
    x = x.where(data_mask,np.nan)
    i_yfine = x.dims.index('y_fine')
    i_xfine = x.dims.index('x_fine')
    res = x.mean(axis=(i_yfine,i_xfine))
    if cover_ocean is not False:
        res = res.where(landmask_coarse,cover_ocean)
    return res

def most_common(data_regions,var_,cover_ocean=False,landmask_coarse=None):
    x = data_regions[var_]
    i_yfine = x.dims.index('y_fine')
    i_xfine = x.dims.index('x_fine')
    i_nz = x.dims.index('z')
    i_ny = x.dims.index('y')
    i_nx = x.dims.index('x')

    vals = np.unique(x)

    # # mask the land out, otherwise coastal cells get assigned water-color
    data_mask = data_regions.LANDMASK
    x = x.where(data_mask,np.nan)

    #initialize return dataset
    grid_return = x.median(axis=(i_yfine,i_xfine))

    grid_most_common = np.zeros(grid_return.shape)
    grid_n_vals = np.zeros(grid_return.shape)

    #loop through each unique value, check number (n) of values per aggregated grid, set to new value if n is larger than previous
    for i1,val_ in enumerate(vals):

        mask_val = (x == val_)
        n_val = mask_val.sum(axis=(i_yfine,i_xfine)).values

        mask_apply = (n_val > grid_n_vals) #>: equal amounts -> favour smaller index; >=: equal amounts -> favour larger index
        grid_most_common[mask_apply] = val_
        grid_n_vals[mask_apply] = n_val[mask_apply]

    grid_return.values = grid_most_common
    # return grid_return
    if cover_ocean is not False:
        grid_return = grid_return.where(landmask_coarse,cover_ocean)
    return grid_return
       
def median_round(data_regions,var_,cover_ocean=False,round_='up'):
    x = data_regions[var_]
    assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
    x_ = x.median(axis=(1,3))
    if round_ == 'down':
         #   x_[x_ < 1] = 0    
        mask = ~(x_<1) #everything smaller than 1 will get assigned sea
        x_ = x_.where(mask).fillna(0)

    elif round_ == 'up':
        # x_[x_ > 0] = 1
        mask = ~(x_ > 0) #everything larger than 0 will get assigned land
        x_ = x_.where(mask).fillna(1)
        
    res = x_
    if cover_ocean is not False:
        res = res.where(landmask_coarse,cover_ocean)
    return res

# def div_n(x):
#     x_ = x / n_coarse
#     return x_[:,0]

# def median_round(x,round_='up'):
#     assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
#     x_ = x.median(axis=(1,3))
#     if round_ == 'down':
#          #   x_[x_ < 1] = 0    
#         mask = ~(x_<1) #everything smaller than 1 will get assigned sea
#         x_ = x_.where(mask).fillna(0)

#     elif round_ == 'up':
#         # x_[x_ > 0] = 1
#         mask = ~(x_ > 0) #everything larger than 0 will get assigned land
#         x_ = x_.where(mask).fillna(1)
        
#     return x_

# def lower_corner(x):
#     assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
#     return x[:,0,:,0]

# def upper_corner(x):
#     assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
#     return x[:,-1,:,-1]

# def centre(x):
#     assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
#     i_take = int(x.shape[1] / 2)
#     assert x.shape[1]%2 == 0
#     return x[:,i_take,:,i_take]

# def sum_cells(x):
#     assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
#     return x.sum(axis=(1,3))

# def mean_cells(x):
#     i_yfine = x.dims.index('y_fine')
#     i_xfine = x.dims.index('x_fine')
#     return x.mean(axis=(i_yfine,i_xfine))

# def most_common(x):
#     assert len(x.dims) == 4, 'TODO: implement fn for depth/time dimensions'
#     vals = np.unique(x)

#     grid_most_common = np.zeros([x.shape[0],x.shape[2]])
#     grid_n_vals = np.zeros([x.shape[0],x.shape[2]])
    
#     #initialize return dataset
#     grid_return = x.median(axis=(1,3))
    
#     #loop through each unique value, check number (n) of values per aggregated grid, set to new value if n is larger than previous
#     for val_ in vals:
#         mask_val = (x == val_)
#         n_val = mask_val.sum(axis=(1,3)).values

#         mask_apply = (n_val > grid_n_vals) #>: equal amounts -> favour smaller index; >=: equal amounts -> favour larger index
#         grid_most_common[mask_apply] = val_
#         grid_n_vals[mask_apply] = n_val[mask_apply]
        
#     grid_return.values = grid_most_common
#     return grid_return